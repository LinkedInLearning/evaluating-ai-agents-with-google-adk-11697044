"""
04_02 -- Trajectory Matching Rules

Runs the agent against three scenarios to manually verify the 3-step
pipeline before formally scoring with `adk eval`.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent

def main():
    print("SCENARIO -- Trajectory Matching Sequences")
    print("=" * 60)

    # 1. Mandatory sequence: all 3 tools called in order
    print("\n--- TEST: MANDATORY PIPELINE ---")
    prompt_mandatory = "I need a 14-inch standard laptop for the engineering department."
    run_agent(root_agent, prompt_mandatory, session_id="mandatory_full")

    # 2. Forbidden sequence: stops early at step 1
    print("\n--- TEST: FORBIDDEN EDGE CASE (CATALOG REJECTS) ---")
    prompt_forbidden_1 = "Can you order a quantum laptop for the engineering department?"
    run_agent(root_agent, prompt_forbidden_1, session_id="forbidden_catalog")

    # 3. Forbidden sequence: stops early at step 2 
    print("\n--- TEST: FORBIDDEN EDGE CASE (BUDGET REJECTS) ---")
    prompt_forbidden_2 = "I need a 14-inch standard laptop for the marketing department."
    run_agent(root_agent, prompt_forbidden_2, session_id="forbidden_budget")

if __name__ == "__main__":
    main()
