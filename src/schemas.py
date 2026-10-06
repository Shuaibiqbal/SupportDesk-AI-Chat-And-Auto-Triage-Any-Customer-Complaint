from pydantic import BaseModel
from typing import Literal

class SupportTicket(BaseModel):
    customer_name: str | None
    issue_category: Literal["billing", "technical", "account_access", "other"]
    urgency:  Literal["low", "medium", "high"]
    summary: str

class RouteDecision(BaseModel):
    agent: Literal["concierge", "triage"]
    reason: str
