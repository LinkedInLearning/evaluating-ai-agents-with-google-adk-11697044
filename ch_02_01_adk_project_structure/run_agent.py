"""
02_01 -- ADK Project Structure

Understands the foundation of the Agent Development Kit (ADK) by decoupling 
the agentic logic and model configuration from raw API calls.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent

def main():
    print("SCENARIO -- Expected: GRACEFUL REFUSAL (no tools attached)")
    print("=" * 60)
    run_agent(root_agent, "I need a 16-inch pro laptop for the engineering department.", session_id="demo")

if __name__ == "__main__":
    main()
