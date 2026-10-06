from src.schemas import SupportTicket

def print_ticket(ticket: SupportTicket) -> None:

    customer_name = ticket.customer_name
    if customer_name is None:
        customer_name = "(not_given)"
    print("Ticket Created.")
    print(f"Customer Name: {customer_name}")
    print(f"Category: {ticket.issue_category}")
    print(f"Urgency: {ticket.urgency}")
    print(f" Summary: {ticket.summary}")