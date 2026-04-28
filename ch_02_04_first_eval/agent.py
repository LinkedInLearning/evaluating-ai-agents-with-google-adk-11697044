"""
02_04 -- First Eval: Did the Agent Call the Right Tool?

Introduces ADK evaluations to deterministically verify if the agent correctly 
triggered the expected tool chain when asked, instead of reading fluctuating text outputs.
"""

import os
import sys
from typing import Dict, Any, Literal
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from helpers import get_mock_db

from google.adk.agents import Agent

_DB = get_mock_db()

# ---------------------------------------------------------------------------
# PYDANTIC SCHEMA CONTRACTS
# ---------------------------------------------------------------------------
class CatalogRequest(BaseModel):
    item_id: str = Field(
        ..., 
        description="The exact corporate identifier of the item.",
        pattern=r'^[a-z0-9_]+$' # Enforce snake_case string, no spaces or capitals
    )

class BudgetRequest(BaseModel):
    department: Literal["engineering", "sales", "marketing", "hr"] = Field(
        ..., 
        description="The strict requesting department enum value."
    )

class OrderRequest(BaseModel):
    item_id: str = Field(..., description="The verified catalog item identifier.")
    department: Literal["engineering", "sales", "marketing", "hr"] = Field(..., description="The validated requesting department.")
    price: float = Field(..., description="The exact float price verified from the catalog. Do not use commas.", ge=0.0)

class RefusalRequest(BaseModel):
    reason: str = Field(..., description="The detailed, professional justification for refusing the request.")

# ---------------------------------------------------------------------------
# ENTERPRISE TOOL CAPABILITIES
# ---------------------------------------------------------------------------
# By processing arguments through Pydantic's `model_validate`, we intercept 
# hallucinations natively. The ValidationError is returned to the agent,
# forcing it to "Observation -> Reason -> Auto-Correct" without crashing.

def check_catalog(req: CatalogRequest) -> Dict[str, Any]:
    """Query the enterprise catalog. Arg must match CatalogRequest schema."""
    try:
        req = CatalogRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
            
    item = req.item_id
    if item in _DB["catalog"]:
        return _DB["catalog"][item]
    return {"error": f"Item '{item}' not found in corporate catalog."}

def check_budget(req: BudgetRequest) -> Dict[str, Any]:
    """Verify budget limits. Arg must match BudgetRequest enum schema."""
    try:
        req = BudgetRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
            
    dept = req.department
    if dept in _DB["budgets"]:
        budget_data = _DB["budgets"][dept]
        policy_data = _DB["policies"].get(dept, {})
        return {
            "cost_center": budget_data.get("cost_center", "UNKNOWN"),
            "remaining_budget": budget_data.get("available", 0),
            "allowed_categories": policy_data.get("allowed_categories", []),
        }
    return {"error": f"Department '{dept}' not found in records."}

def place_order(req: OrderRequest) -> Dict[str, Any]:
    """Execute transaction log. Arg must match OrderRequest schema."""
    try:
        req = OrderRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
            
    return {
        "status": "success", 
        "transaction_id": f"TXN-{os.urandom(4).hex().upper()}",
        "message": f"Procurement order placed: {req.item_id} at ${req.price:.2f} for {req.department}."
    }

def refuse_request(req: RefusalRequest) -> Dict[str, Any]:
    """Log formal refusal. Arg must match RefusalRequest schema."""
    try:
        req = RefusalRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
            
    return {
        "status": "refused", 
        "audit_flag": "POLICY_VIOLATION",
        "reason": req.reason
    }

# ---------------------------------------------------------------------------
# AGENT DEFINITION
# ---------------------------------------------------------------------------
root_agent = Agent(
    name="pydantic_procurement_agent",
    description="A procurement agent strictly adhering to Pydantic tool schemas.",
    model="gemini-3-flash-preview",
    instruction=(
        "You are an Enterprise Procurement Agent.\n\n"
        "STANDARD OPERATING PROCEDURE (SOP):\n"
        "1. Catalog Validation: Always call `check_catalog` to verify the item exists, determine its price, and evaluate if it is restricted.\n"
        "2. Budget Validation: Always call `check_budget` to ensure the requesting department has sufficient `remaining_budget` and is authorized for the item's `category`.\n"
        "3. Rejection Path: If the item is restricted, the budget is insufficient, or the category is unauthorized, you MUST immediately call `refuse_request`.\n"
        "4. Execution Path: ONLY if all preceding checks pass and the item is fully compliant may you call `place_order`.\n\n"
        "AUTO-CORRECTION PROTOCOL:\n"
        "If you receive a 'Schema Validation Error', do NOT immediately refuse the request. "
        "Instead, carefully read the regex or enum rule in the error, auto-correct the human's dirty input "
        "(e.g. converting 'Laptop Pro 16' to 'laptop_pro_16' or 'Eng' to 'engineering'), and retry the tool."
    ),
    tools=[check_catalog, check_budget, place_order, refuse_request]
)
