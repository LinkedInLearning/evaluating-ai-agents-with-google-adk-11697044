"""
02_03 -- Schema as a Contract: Pydantic Enforcement

Eradicates LLM argument hallucinations (e.g., passing "Eng" instead of "engineering") 
by enforcing strict Pydantic schemas at the tool boundaries.
"""

import sys
from pathlib import Path

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo, run_agent
init_demo()

from agent import root_agent

def main():
    dirty_prompt = ">>hey can you order me a pro lptp 16 for the eng dept? thx"
    
    print("SCENARIO -- Expected: Pydantic auto-correction of dirty input")
    print("=" * 60)
    
    run_agent(root_agent, dirty_prompt, session_id="demo")

if __name__ == "__main__":
    main()
