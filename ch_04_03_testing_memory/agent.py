"""
04_03 -- Testing Memory: Context Persistence

Defines an agent that requires a 'department' field to place an order.
This is used to demonstrate memory decay if the user provides their department
early in a long-horizon conversation.
"""

import os
import json
from typing import Dict, Any, Literal
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
from google.adk.agents import Agent

# ---------------------------------------------------------------------------
# SHARED DATA SOURCE
# ---------------------------------------------------------------------------
_DB_PATH = Path(__file__).resolve().parent.parent / "mock_data.json"
with open(_DB_PATH, "r") as _f:
    _DB = json.load(_f)

# ---------------------------------------------------------------------------
# PYDANTIC SCHEMA CONTRACTS
# ---------------------------------------------------------------------------
class SearchRequest(BaseModel):
    category: str = Field(..., description="E.g., 'hardware', 'software'.")
    subcategory: str = Field(..., description="E.g., 'laptops', 'av_equipment'.")

class OrderRequest(BaseModel):
    item_id: str = Field(..., description="The verified catalog item identifier.")
    department: Literal["engineering", "sales", "marketing", "hr", "executive", "security", "it_infrastructure"] = Field(
        ...,
        description="The asking user's exact department. DO NOT GUESS if unknown."
    )

# ---------------------------------------------------------------------------
# TOOLS
# ---------------------------------------------------------------------------
def lookup_catalog(req: SearchRequest) -> Dict[str, Any]:
    """Search the enterprise catalog by category and subcategory."""
    try:
        req = SearchRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}

    results = []
    for sku, data in _DB["catalog"].items():
        if data.get("category") == req.category and data.get("subcategory") == req.subcategory:
            results.append({
                "item_id": sku,
                "description": data["description"],
                "price": data["price"]
            })
    
    if not results:
        return {"status": "NOT_FOUND", "message": "No items found matching the criteria."}
    
    return {"status": "SUCCESS", "results": results}

def place_order(req: OrderRequest) -> Dict[str, Any]:
    """Execute the procurement order. REQUIRES the user's department."""
    try:
        req = OrderRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}

    item = _DB["catalog"].get(req.item_id)
    if item is None:
        return {"status": "FAILED", "reason": f"Item '{req.item_id}' not found."}

    return {
        "status": "SUCCESS",
        "message": f"Order for {req.item_id} confirmed for {req.department} department.",
        "transaction_id": f"TXN-{os.urandom(4).hex().upper()}"
    }

# ---------------------------------------------------------------------------
# AGENT DEFINITION
# ---------------------------------------------------------------------------
root_agent = Agent(
    name="memory_test_agent",
    description="Corporate procurement agent to test long context retention.",
    model="gemini-3-flash-preview",
    instruction=(
        "You are an enterprise procurement agent.\n\n"
        "STANDARD OPERATING PROCEDURE:\n"
        "1. You can search for products using `lookup_catalog`.\n"
        "2. To place an order, use `place_order`. This REQUIRES you to specify the user's `department`.\n"
        "3. You MUST NEVER GUESS the user's department. If the user hasn't told you their department, you must ask for it explicitly before ordering.\n"
        "4. Keep your responses short and professional."
    ),
    tools=[lookup_catalog, place_order]
)
