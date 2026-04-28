"""
04_03 -- Testing Memory: Context Persistence

Script to demonstrate how the agent behaves in a multi-turn conversation.
We provide the 'department' context early on, then flood the context window
with noise, and finally attempt to purchase to see if it remembers.
"""

import sys
from pathlib import Path
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import init_demo
init_demo()

from agent import root_agent

def run_multi_turn_demo():
    print("SCENARIO -- Context Persistence & Memory Decay")
    print("=" * 60)
    
    runner = InMemoryRunner(agent=root_agent)
    runner.auto_create_session = True
    session_id = "long_horizon_002"
    
    # The simulated user conversation
    user_prompts = [
        # Turn 1: Setting the context
        "Hi, I'm a new employee in the engineering department. Nice to meet you.",
        
        # Turn 2: Noise to flush context
        "In the 'hardware' category, what 'laptops' are available?",
        
        # Turn 3: More noise
        "I also heard we have 'av_equipment' in the 'hardware' category. Can you list it?",
        
        # Turn 4: The memory test
        "Nevermind the AV stuff. Just order me the 16-inch pro laptop."
    ]
    
    for turn_idx, text in enumerate(user_prompts, start=1):
        print(f"\n[TURN {turn_idx}] USER: {text}")
        
        content = Content(role="user", parts=[Part.from_text(text=text)])
        
        final_text = ""
        tool_calls = []
        
        # We run the agent and preserve session history
        for event in runner.run(user_id="demo", session_id=session_id, new_message=content):
            if not (hasattr(event, "content") and event.content and event.content.parts):
                continue
                
            for part in event.content.parts:
                if getattr(part, "function_call", None):
                    tool_calls.append(part.function_call.name)
                elif getattr(part, "text", None) and part.text.strip():
                    final_text += part.text

        final_text = final_text.strip()
        if final_text:
            print(f"  AGENT: {final_text}")
        if tool_calls:
            print(f"  TRAJECTORY: {tool_calls}")
        else:
            print(f"  TRAJECTORY: [] (No tools called)")

def main():
    run_multi_turn_demo()

if __name__ == "__main__":
    main()
