"""Shared helpers for running agents and evaluations across all chapters."""

import os
import sys
import json
import io
import logging
import subprocess
import re
import warnings
# Suppress ALL warnings before any import — authlib/ADK emit at import time.
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", message="authlib.jose module is deprecated")
from pathlib import Path

# Silence ADK import-time log noise, then re-enable for runtime.
logging.disable(logging.WARNING)
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part
logging.disable(logging.NOTSET)

_REPO_ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# STDOUT FILTER — suppresses ADK's print()-based "non-text parts" message
# ---------------------------------------------------------------------------
_ADK_NOISE = {
    "Warning: there are non-text parts", 
    "authlib.jose module is deprecated",
    "Failed to convert argument"
}

class _CleanStdout:
    """Wraps sys.stdout to swallow known ADK noise lines."""
    def __init__(self, stream):
        self._s = stream
        self._buf = ""

    def write(self, text):
        self._buf += text
        if "\n" in self._buf:
            lines = self._buf.split("\n")
            for line in lines[:-1]:
                if not any(noise in line for noise in _ADK_NOISE):
                    self._s.write(line + "\n")
            self._buf = lines[-1]

    def flush(self):
        if self._buf and not any(noise in self._buf for noise in _ADK_NOISE):
            self._s.write(self._buf)
        self._buf = ""
        self._s.flush()

    def __getattr__(self, name):
        return getattr(self._s, name)


# ---------------------------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------------------------
def init_demo():
    """Load API keys from .env and suppress verbose ADK logs."""
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=_REPO_ROOT / ".env")

    if not os.environ.get("GOOGLE_API_KEY") and not os.environ.get("GEMINI_API_KEY"):
        sys.exit("ERROR: GOOGLE_API_KEY not found. Set it in the root .env file")

    logging.getLogger("google.genai").setLevel(logging.ERROR)
    logging.getLogger("google.adk").setLevel(logging.ERROR)


def get_mock_db() -> dict:
    """Load the shared mock database (mock_data.json)."""
    with open(_REPO_ROOT / "mock_data.json", "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# AGENT RUNNER (ch_01 -- ch_04)
# ---------------------------------------------------------------------------
def run_agent(agent, prompt, *, session_id="default"):
    """Run an agent with a single prompt. Returns (trajectory, final_text)."""
    print(f"  USER: {prompt}")
    runner = InMemoryRunner(agent=agent)
    runner.auto_create_session = True

    content = Content(role="user", parts=[Part.from_text(text=prompt)])
    final_text = ""
    tool_calls = []

    _orig_stdout = sys.stdout
    _orig_stderr = sys.stderr
    sys.stdout = _CleanStdout(_orig_stdout)
    sys.stderr = _CleanStdout(_orig_stderr)
    try:
      events = list(runner.run(user_id="demo", session_id=session_id, new_message=content))
    finally:
      sys.stdout.flush()
      sys.stderr.flush()
      sys.stdout = _orig_stdout
      sys.stderr = _orig_stderr

    for event in events:
        if not (hasattr(event, "content") and event.content and event.content.parts):
            continue
        for part in event.content.parts:
            if getattr(part, "function_call", None):
                tool_calls.append(part.function_call.name)
                print(f"  [TOOL CALL]    {part.function_call.name}({part.function_call.args})")
            elif getattr(part, "function_response", None):
                print(f"  [OBSERVATION]  {part.function_response.name} -> {part.function_response.response}")
            elif getattr(part, "text", None) and part.text.strip():
                final_text += part.text

    final_text = final_text.strip()
    if final_text:
        print(f"\n  AGENT: {final_text}")
    print(f"  TRAJECTORY: {tool_calls}\n")
    return tool_calls, final_text


# ---------------------------------------------------------------------------
# ADK EVAL UTILITIES (ch_05 -- ch_06)
# ---------------------------------------------------------------------------
def run_adk_eval(agent_module: str, evalset_path: str, config_path: str) -> dict:
    """Run `adk eval` via CLI and return parsed pass/fail counts."""
    cmd = [
        sys.executable, "-m", "google.adk.cli",
        "eval", agent_module, evalset_path,
        f"--config_file_path={config_path}",
    ]

    result = subprocess.run(
        cmd, cwd=str(_REPO_ROOT),
        capture_output=True, text=True, timeout=300,
    )

    output = result.stdout + result.stderr
    passed = failed = 0
    m = re.search(r"Tests passed:\s*(\d+)", output)
    if m:
        passed = int(m.group(1))
    m = re.search(r"Tests failed:\s*(\d+)", output)
    if m:
        failed = int(m.group(1))

    return {"passed": passed, "failed": failed, "output": output}


def parse_eval_results(chapter_dir: Path) -> list:
    """Read ADK eval history and return per-case results with rubric/groundedness scores."""
    history_dir = chapter_dir / ".adk" / "eval_history"
    if not history_dir.exists():
        return []

    result_files = sorted(history_dir.glob("*.evalset_result.json"))
    if not result_files:
        return []

    results = []
    for f in result_files:
        data = json.loads(f.read_text())
        for case in data.get("eval_case_results", []):
            rubric_scores = []
            groundedness_score = None
            for metric in case.get("overall_eval_metric_results", []):
                if metric.get("metric_name") == "hallucinations_v1":
                    groundedness_score = metric.get("score")
                details = metric.get("details") or {}
                for rs in details.get("rubric_scores") or []:
                    rubric_scores.append({"rubric_id": rs["rubric_id"], "score": rs["score"]})
            results.append({
                "eval_id": case.get("eval_id", "unknown"),
                "passed": case.get("final_eval_status") == 1,
                "rubric_scores": rubric_scores,
                "groundedness_score": groundedness_score,
            })
    return results


def clean_eval_history(chapter_dir: Path):
    """Remove previous eval history so only fresh results are shown."""
    history_dir = chapter_dir / ".adk" / "eval_history"
    if history_dir.exists():
        for f in history_dir.glob("*.json"):
            f.unlink()
