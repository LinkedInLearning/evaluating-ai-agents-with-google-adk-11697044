"""
03_03 -- Visual Debugging with ADK Trace View

Steps through failed agent trajectories using the visual ADK Trace Viewer
to pinpoint looping, stalling, or hallucinated re-planning errors.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent

def main():
    print("SCENARIO -- Expected: STALL / RE-PLANNING LOOP TRAP")
    print("=" * 60)
    
    run_agent(
        root_agent, 
        "Check if my laptop transaction TXN-1234 has been approved.", 
        session_id="loop_debug"
    )

if __name__ == "__main__":
    main()
