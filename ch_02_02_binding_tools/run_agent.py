"""
02_02 -- Binding Tools to the Agent

Expands the base Agent by providing it with four enterprise Python functions.
The ADK automatically interprets the docstrings of these functions and natively 
generates the JSON tool schemas required by the Gemini LLM.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent

def main():
    print("SCENARIO -- Expected: APPROVED (tools are bound and active)")
    print("=" * 60)
    run_agent(root_agent, "I need a 16-inch pro laptop for the engineering department.", session_id="demo")

if __name__ == "__main__":
    main()
