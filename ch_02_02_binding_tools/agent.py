"""
02_02 -- Binding Tools to the Agent

Expands the base Agent by providing it with four enterprise Python functions.
The ADK automatically interprets the docstrings of these functions and natively 
generates the JSON tool schemas required by the Gemini LLM.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add parent dir so we can import shared helpers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from helpers import get_mock_db

from google.adk.agents import Agent

# ---------------------------------------------------------------------------
# DATA ACCESS LAYER (MOCK)
# ---------------------------------------------------------------------------
_DB = get_mock_db()

# ---------------------------------------------------------------------------
# ENTERPRISE TOOL CAPABILITIES
# ---------------------------------------------------------------------------
def check_catalog(item_id: str) -> Dict[str, Any]:
    """
    Query the enterprise procurement catalog for item specifications and restrictions.
    
    Args:
        item_id: The unique identifier of the item in the catalog (e.g., 'laptop_pro_16').
    """
    normalized_item = item_id.lower().strip()
    if normalized_item in _DB["catalog"]:
        return _DB["catalog"][normalized_item]
    return {"error": f"Item '{item_id}' not found in the approved corporate catalog."}

def check_budget(department: str) -> Dict[str, Any]:
    """
    Verify the remaining budget allocation and allowed spending categories for a Cost Center.
    
    Args:
        department: The name of the department/cost center (e.g., 'engineering', 'sales').
    """
    dept = department.lower().strip()
    if dept in _DB["budgets"]:
        budget_data = _DB["budgets"][dept]
        policy_data = _DB["policies"].get(dept, {})
        remaining_funds = budget_data.get("available", 0)
        allowed_categories = policy_data.get("allowed_categories", [])
        return {
            "cost_center": budget_data.get("cost_center", "UNKNOWN"),
            "remaining_budget": remaining_funds,
            "allowed_categories": allowed_categories,
        }
    return {"error": f"Department '{department}' not found in financial records."}

def place_order(item_id: str, department: str, price: float) -> Dict[str, Any]:
    """
    Execute the procurement transaction. 
    MUST ONLY be called after catalog and budget validations have succeeded.
    
    Args:
        item_id: The catalog item identifier.
        department: The requesting department.
        price: The exact price verified from the catalog.
    """
    return {
        "status": "success", 
        "transaction_id": f"TXN-{os.urandom(4).hex().upper()}",
        "message": f"Procurement order placed: {item_id} at ${price:.2f} for {department}."
    }

def refuse_request(reason: str) -> Dict[str, Any]:
    """
    Log and issue a formal refusal for a procurement request that violates corporate policy.
    
    Args:
        reason: The detailed justification for refusing the request.
    """
    return {
        "status": "refused", 
        "audit_flag": "POLICY_VIOLATION",
        "reason": reason
    }

# ---------------------------------------------------------------------------
# AGENT DEFINITION (Tools Bound!)
# ---------------------------------------------------------------------------
# The ADK parses our python functions and docstrings, converts them into 
# native schemas, and injects them seamlessly into the Gemini execution.
root_agent = Agent(
    name="baseline_root_agent",
    description="A basic procurement agent equipped with firm-wide database tools.",
    model="gemini-3-flash-preview",
    instruction=(
        "You are an Enterprise Procurement Agent.\n\n"
        "STANDARD OPERATING PROCEDURE (SOP):\n"
        "1. Catalog Validation: Always call `check_catalog` to verify the item exists, determine its price, and evaluate if it is restricted.\n"
        "2. Budget Validation: Always call `check_budget` to ensure the requesting department has sufficient `remaining_budget` and is authorized for the item's `category`.\n"
        "3. Rejection Path: If the item is restricted, the budget is insufficient, or the category is unauthorized, you MUST immediately call `refuse_request`.\n"
        "4. Execution Path: ONLY if all preceding checks pass and the item is fully compliant may you call `place_order`."
    ),
    tools=[check_catalog, check_budget, place_order, refuse_request]
)
