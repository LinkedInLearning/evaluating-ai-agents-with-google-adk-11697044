"""
04_01 -- Capturing Golden Traces

This script executes a verified "Golden" trace where the AI correctly achieves
the target objective by using its tools in the exact requested order.
We will then capture this trace via the ADK UI to serve as a baseline.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent

def main():
    print("SCENARIO -- Expected: PERFECT PROCUREMENT WORKFLOW")
    print("=" * 60)
    
    # 1. We trigger the optimal workflow (Happy Path).
    print("\n--- TEST: HAPPY PATH ---")
    prompt_success = (
        "I have a laptop purchase request for a 'high-end engineering workstation laptop' with a "
        "budget of $3000. My transaction approval ID is TXN-1234. Please buy it."
    )
    run_agent(root_agent, prompt_success, session_id="golden_trace_demo")

    # 2. We trigger the negative/edge-case failure workflow (Non-Happy Path).
    print("\n--- TEST: NON-HAPPY PATH (EDGE CASE) ---")
    prompt_fail = (
        "I need a laptop. My transaction ID is ABC-999. Can you approve it?"
    )
    run_agent(root_agent, prompt_fail, session_id="negative_trace_demo")

if __name__ == "__main__":
    main()
