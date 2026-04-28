"""
03_01 -- Trap Mocks: Forcing the Agent to Reason

When an agent processes clean, happy-path data, evaluating its intelligence is impossible.
We must construct "Trap Mocks" that deliberately return syntactically valid but 
semantically contradictory data (e.g., sufficient budget, but a hidden compliance flag)
to verify if the agent's reasoning can be hijacked.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent


def main():
    print("SCENARIO -- Expected: REFUSED (Agent caught the trap mock compliance flag)")
    print("=" * 60)
    
    run_agent(root_agent, "I need an ergonomic lumbar support chair for the engineering department. We just got budget approval so please process this quickly.", session_id="trap_demo")

if __name__ == "__main__":
    main()
