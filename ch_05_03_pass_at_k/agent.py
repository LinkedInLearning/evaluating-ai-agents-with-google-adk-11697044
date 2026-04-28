"""
05_03 -- Pass@k and Non-Determinism

The same Pydantic-enforced procurement agent used across this course.
This chapter focuses on measuring statistical reliability, not modifying
agent logic.
"""

import os
import json
from typing import Dict, Any, Literal
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
from google.adk.agents import Agent

# ---------------------------------------------------------------------------
# SHARED DATA SOURCE (loaded from central mock_data.json)
# ---------------------------------------------------------------------------
_DB_PATH = Path(__file__).resolve().parent.parent / "mock_data.json"
with open(_DB_PATH, "r") as _f:
    _DB = json.load(_f)

# ---------------------------------------------------------------------------
# PYDANTIC SCHEMA CONTRACTS
# ---------------------------------------------------------------------------
class CatalogRequest(BaseModel):
    item_id: str = Field(
        ...,
        description="The exact corporate catalog identifier (e.g. 'laptop_pro_16').",
        pattern=r'^[a-z0-9_]+$'
    )

class BudgetRequest(BaseModel):
    department: Literal[
        "engineering", "marketing", "sales", "hr", "executive",
        "security", "it_infrastructure", "product"
    ] = Field(
        ...,
        description="The requesting department (enum value)."
    )

class OrderRequest(BaseModel):
    item_id: str = Field(..., description="The verified catalog item identifier.")
    department: Literal[
        "engineering", "marketing", "sales", "hr", "executive",
        "security", "it_infrastructure", "product"
    ] = Field(
        ...,
        description="The validated requesting department."
    )
    price: float = Field(
        ...,
        description="The exact price verified from the catalog.",
        ge=0.0
    )

class RefuseRequest(BaseModel):
    reason: str = Field(
        ...,
        description="The detailed, professional justification for refusing the request."
    )

# ---------------------------------------------------------------------------
# TOOLS (3-Step Pipeline backed by shared data)
# ---------------------------------------------------------------------------
def check_catalog(req: CatalogRequest) -> Dict[str, Any]:
    """Look up an item in the corporate procurement catalog by its item_id."""
    try:
        req = CatalogRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}

    item = _DB["catalog"].get(req.item_id)
    if item is None:
        return {"status": "NOT_FOUND", "message": f"'{req.item_id}' not found in corporate catalog."}

    return {
        "item_id": req.item_id,
        "sku": item["sku"],
        "price": item["price"],
        "description": item["description"],
        "inventory_status": item["inventory_status"],
        "restricted": item.get("restricted", False),
    }

def check_budget(req: BudgetRequest) -> Dict[str, Any]:
    """Verify budget availability for a department."""
    try:
        req = BudgetRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}

    budget = _DB["budgets"].get(req.department)
    if budget is None:
        return {"status": "NOT_FOUND", "message": f"No budget record for '{req.department}'."}

    if budget.get("freeze_status"):
        return {
            "status": "FROZEN",
            "department": req.department,
            "reason": budget.get("freeze_reason", "Budget is frozen."),
        }
    return {
        "department": req.department,
        "cost_center": budget["cost_center"],
        "available": budget["available"],
        "currency": budget["currency"],
    }

def place_order(req: OrderRequest) -> Dict[str, Any]:
    """Execute the procurement order after catalog and budget validation."""
    try:
        req = OrderRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}

    # Verify the item exists and is in stock
    item = _DB["catalog"].get(req.item_id)
    if item is None:
        return {"status": "FAILED", "reason": f"Item '{req.item_id}' not found."}

    if item["inventory_status"] != "in_stock":
        return {"status": "FAILED", "reason": f"Item is '{item['inventory_status']}', cannot fulfill."}

    return {
        "status": "SUCCESS",
        "transaction_id": f"TXN-{os.urandom(4).hex().upper()}",
        "item": req.item_id,
        "price": req.price,
        "department": req.department,
    }

def refuse_request(req: RefuseRequest) -> Dict[str, Any]:
    """Refuse a procurement request and log the policy violation."""
    try:
        req = RefuseRequest.model_validate(req)
    except ValidationError as e:
        return {"error": f"Schema Validation Error: {e.errors()}"}
    return {"status": "refused", "audit_flag": "POLICY_VIOLATION", "reason": req.reason}

# ---------------------------------------------------------------------------
# AGENT DEFINITION
# ---------------------------------------------------------------------------
root_agent = Agent(
    name="pass_at_k_agent",
    description="Procurement agent used for Pass@k reliability measurement.",
    model="gemini-3-flash-preview",
    instruction=(
        "You are an enterprise procurement agent.\n\n"
        "STANDARD OPERATING PROCEDURE (3-step pipeline):\n"
        "1. CATALOG: Always call `check_catalog` first to verify the item exists, "
        "get its price, and check its inventory status.\n"
        "2. BUDGET: Only if the item is 'in_stock' and not restricted, "
        "call `check_budget` to verify the department has available funds.\n"
        "3. ORDER: Only if the budget is sufficient and not frozen, "
        "call `place_order` with the verified price.\n\n"
        "FORBIDDEN ACTIONS:\n"
        "- Do NOT call `check_budget` if the item is not in stock or is restricted.\n"
        "- Do NOT call `place_order` if the budget is frozen or insufficient.\n"
        "- Do NOT skip any step in the pipeline.\n\n"
        "AUTO-CORRECTION PROTOCOL:\n"
        "If you receive a 'Schema Validation Error', do NOT give up. "
        "Read the regex or enum rule in the error, auto-correct the user's input "
        "(e.g. converting '14-inch standard laptop' to 'laptop_std_14' or 'Eng' to 'engineering'), "
        "and retry the tool.\n\n"
        "Always inform the user of the reason if a step fails."
    ),
    tools=[check_catalog, check_budget, place_order, refuse_request],
)
