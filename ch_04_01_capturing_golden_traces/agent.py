"""
04_01 -- Capturing Golden Traces

Demonstrates how to run a successfully verified agent trajectory 
and establish it as a "Golden Trace" regression test.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError
from google.adk.agents import Agent

# ---------------------------------------------------------------------------
# PYDANTIC SCHEMA CONTRACTS
# ---------------------------------------------------------------------------
class StatusRequest(BaseModel):
    transaction_id: str = Field(
        ..., 
        description="The exact transaction ID to verify."
    )

class PurchaseRequest(BaseModel):
    item_name: str = Field(..., description="Name of the item to purchase.")
    budget: float = Field(..., description="Maximum budget allocated.")

# ---------------------------------------------------------------------------
# FUNCTIONAL TOOLS (The Target Trace Logic)
# ---------------------------------------------------------------------------
def check_approval_status(req: StatusRequest) -> Dict[str, Any]:
    """Check the asynchronous status of a pending transaction."""
    try:
        req = StatusRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
    
    # EDGE CASE HANDLING: Validate logical bounds instead of blindly mocking success.
    if not req.transaction_id.startswith("TXN-"):
        return {"status": "INVALID_FORMAT", "message": "Transaction IDs must start with 'TXN-'"}
    
    if req.transaction_id != "TXN-1234":
        return {"status": "NOT_FOUND", "message": f"No record found for {req.transaction_id}."}
        
    # We simulate a definitively APPROVED state for the golden path.
    return {
        "transaction_id": req.transaction_id,
        "status": "approved",
        "message": "Transaction fully vertically approved by management."
    }

def purchase_equipment(req: PurchaseRequest) -> Dict[str, Any]:
    """Execute the purchase of approved equipment if within budget."""
    try:
        req = PurchaseRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
    
    # EDGE CASE HANDLING: System-level validation
    if req.budget <= 0:
        return {"status": "INVALID_BUDGET", "reason": "Allocated budget must be greater than $0."}
    
    if req.budget >= 1500.00:
        return {"status": "SUCCESS", "receipt_id": "REC-9988", "item": req.item_name}
    else:
        return {"status": "FAILED", "reason": "Insufficient budget to meet enterprise hardware standards."}

# ---------------------------------------------------------------------------
# AGENT DEFINITION
# ---------------------------------------------------------------------------
root_agent = Agent(
    name="procurement_agent",
    description="Corporate procurement agent.",
    model="gemini-3-flash-preview",
    instruction=(
        "You are an enterprise procurement agent.\n\n"
        "STANDARD OPERATING PROCEDURE:\n"
        "1. If a user asks you to purchase an item, YOU MUST FIRST call `check_approval_status` "
        "using their provided transaction ID.\n"
        "2. Only if the status is exactly 'approved', proceed to call `purchase_equipment`.\n"
        "3. Provide the user with the final receipt ID."
    ),
    tools=[check_approval_status, purchase_equipment]
)
