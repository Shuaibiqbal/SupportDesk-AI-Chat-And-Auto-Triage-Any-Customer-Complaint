from src.schemas import SupportTicket, RouteDecision
from pydantic import ValidationError
def test_ticket_without_a_name() -> None:
    ticket = SupportTicket(
        customer_name= None,
        issue_category="account_access",
        urgency="medium",
        summary="Customer Can't log in after two password reset"
    )
    result = "OK"

    if ticket.customer_name is not None:
        result = "WRONG"
    print(f"Case 1: (no name allowed) --> {result}")

def test_ticket_rejects_unkown_urgency() -> None:
    result = "WRONG"

    try:
        SupportTicket(
            customer_name= "Shuaib Iqbal",
            issue_category="billing",
            urgency="urgent",
            summary="Charged twice in a month"
        )
    except ValidationError:
        result = "OK"
    print(f"Case 2: (bad urgnecy) --> {result}")

def test_route_rejects_unknown_agent() -> None:
    result = "WRONG"
    try:
        RouteDecision(agent="billing", reason="looks like billing")
    except ValidationError:
        result = "OK"
    print(f"Case 3 (bad agent name) -> {result}")
        
if __name__ == "__main__":
    test_ticket_without_a_name()
    test_ticket_rejects_unkown_urgency()
    test_route_rejects_unknown_agent()