"""
01_02 -- The Procurement Agent: Running a Procurement Agent

Defines the ReAct-pattern agent with polished, production-grade tool contracts
and standard operating procedures (SOP).
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent


def main():
    # Scenario A: Marketing orders a laptop -- not eligible department. -> REFUSED.
    print("SCENARIO A -- Expected: REFUSED (department not eligible)")
    print("=" * 60)
    run_agent(root_agent, "I need to order a Laptop Pro 16 for the marketing department.", session_id="a")

    # Scenario B: Engineering orders a laptop -- $93,000 remaining. -> APPROVED.
    print("SCENARIO B -- Expected: APPROVED (within budget)")
    print("=" * 60)
    run_agent(root_agent, "I need to order a 16-inch pro laptop for the engineering department.", session_id="b")


if __name__ == "__main__":
    main()
