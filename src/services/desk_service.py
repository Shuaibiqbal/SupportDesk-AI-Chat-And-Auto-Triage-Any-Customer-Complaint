from src.schemas import SupportTicket

from openai import OpenAI
from src.utils.logger import get_logger
from src.agents.concierge import concierge_agent
from src.agents.triage import triage_agent
from src.agents.router import decide

def print_ticket(ticket: SupportTicket) -> None:

    customer_name = ticket.customer_name
    if customer_name is None:
        customer_name = "(not_given)"
    print("Ticket Created.")
    print(f"Customer Name: {customer_name}")
    print(f"Category: {ticket.issue_category}")
    print(f"Urgency: {ticket.urgency}")
    print(f" Summary: {ticket.summary}")
def handle_message(client: OpenAI, history: list[dict], message: str) -> None:
    logger = get_logger(__name__)
    decision = decide(client=client, message=message)

    if decision.agent == "triage":
        ticket = triage_agent(client, message)
        if ticket is None:
            print("Sorry, I could not turn that into ticket - please")
            print("describe the problem in a little more details.")
        else:
            logger.info(f"ticket: {ticket.issue_category} / {ticket.urgency}")
            print(ticket)
    else:
        print("Concierge: ", end="", flush=True)
        concierge_agent(client,history, message)