"""
02_04 -- First Eval: Did the Agent Call the Right Tool?

Introduces ADK evaluations to deterministically verify if the agent correctly
triggered the expected tool chain when asked.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent


def main():
    # Scenario A -- Happy Path: Engineering orders a laptop.
    # Expected: APPROVED -- trajectory: check_catalog -> check_budget -> place_order
    print("SCENARIO A -- Happy Path")
    print("=" * 60)
    run_agent(root_agent, "I need a 16-inch pro laptop for the engineering department.", session_id="a")

    # Scenario B -- Edge Case: Marketing orders a laptop (budget frozen at -$100).
    # Expected: REFUSED -- trajectory: check_catalog -> check_budget -> refuse_request
    print("SCENARIO B -- Budget Frozen")
    print("=" * 60)
    run_agent(root_agent, "Can you order a 16-inch pro laptop for the marketing team?", session_id="b")

    # Scenario C -- Edge Case: Sloppy input requires Pydantic auto-correction.
    # Expected: APPROVED -- trajectory: check_catalog -> check_budget -> place_order
    print("SCENARIO C -- Auto-correction")
    print("=" * 60)
    run_agent(root_agent, ">>hey can you order me a pro 16 lptp for the eng dept? thx", session_id="c")


if __name__ == "__main__":
    main()
