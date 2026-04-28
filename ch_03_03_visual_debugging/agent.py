"""
03_03 -- Visual Debugging with ADK Trace View

Steps through failed agent trajectories using the visual ADK Trace Viewer
to pinpoint looping, stalling, or hallucinated re-planning errors.
"""

import os
from pathlib import Path
from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError
from google.adk.agents import Agent

# Load API key when imported directly by adk web (bypasses run_agent.py/init_demo)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
except ImportError:
    pass

# ---------------------------------------------------------------------------
# PYDANTIC SCHEMA CONTRACTS
# ---------------------------------------------------------------------------
class StatusRequest(BaseModel):
    transaction_id: str = Field(
        ..., 
        description="The exact transaction ID to verify."
    )

# ---------------------------------------------------------------------------
# MALFUNCTIONING TRAP MOCK (Infinite Loop Generator)
# ---------------------------------------------------------------------------
# This mock intentionally simulates an unresponsive or permanently pending 
# downstream service. It is designed to force the naive agent into an 
# infinite retry loop to demonstrate visual trace stalling.

# Per-transaction call counts — resets automatically after SYSTEM_TIMEOUT
# so each new adk web session gets a fresh counter for the same TXN ID.
_call_counts: Dict[str, int] = {}

def check_approval_status(req: StatusRequest) -> Dict[str, Any]:
    """Check the asynchronous status of a pending transaction."""
    try:
        req = StatusRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
    
    txn = req.transaction_id
    _call_counts[txn] = _call_counts.get(txn, 0) + 1

    if _call_counts[txn] > 4:
        _call_counts[txn] = 0  # reset so next session starts fresh
        return {"error": "SYSTEM_TIMEOUT: You have entered a re-planning stall loop. Stop checking and immediately inform the user that the system is unresponsive."}
    
    # THE TRAP: Never resolves to 'approved'. Permanently pending.
    return {
        "transaction_id": req.transaction_id,
        "status": "pending_manager_approval",
        "message": "Approval is still pending. Instructed to wait and check again momentarily."
    }

# ---------------------------------------------------------------------------
# AGENT DEFINITION
# ---------------------------------------------------------------------------
root_agent = Agent(
    name="looping_process_agent",
    description="An agent prone to infinite looping on pending statuses.",
    model="gemini-3-flash-preview",
    instruction=(
        "You are an asynchronous process monitor.\n\n"
        "STANDARD OPERATING PROCEDURE:\n"
        "1. If a user asks you to verify an order's approval, call `check_approval_status`.\n"
        "2. If the status is 'pending_manager_approval', you MUST keep calling the tool "
        "repeatedly until the status changes to 'approved' before responding to the user.\n"
        "3. Do not stop checking. Do not ask for permission to check again. Just loop the check."
    ),
    tools=[check_approval_status]
)
