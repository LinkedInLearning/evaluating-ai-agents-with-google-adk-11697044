"""
02_01 -- ADK Project Structure

Understands the foundation of the Agent Development Kit (ADK) by decoupling 
the agentic logic and model configuration from raw API calls.
"""

from google.adk.agents import Agent

# ---------------------------------------------------------------------------
# AGENT DEFINITION (No tools bound)
# ---------------------------------------------------------------------------
root_agent = Agent(
    name="root_agent",
    description="A basic procurement agent without tools attached.",
    model="gemini-3-flash-preview",
    instruction="""
    You are an Enterprise Procurement Agent. 
    A user will ask you to buy something. Since you do not currently have access 
    to your database tools, politely explain that you are still being configured 
    by the engineering team and cannot place orders yet. 
    
    If they mention a specific item, acknowledge the item but firmly state you 
    cannot look it up or buy it today.
    """
)
