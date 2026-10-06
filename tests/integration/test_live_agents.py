from src.config import load_config
from src.models.llm import check_api_key_at_startup, create_client, send_message
from openai import OpenAI

# Step 3
from src.agents.triage import triage_agent
from src.config import load_config
import json 
from src.services.desk_service import decide

def test_first_reply(client: OpenAI) -> None:
    reply = send_message(client, [], "What's 2+2?")
    result = "OK"
    if "4" not in reply:
        result = "WRONG"
    print(f"Case 1 (first reply) -> {result}: {reply}")

def test_bad_key() -> None:
    bad_client = OpenAI(api_key="sk-test-123")

    result = "OK"
    if check_api_key_at_startup(bad_client):
        result = "WRONG"
    print(f"Case 2 (bad key) -> {result}")

def test_memory(client: OpenAI) -> None:
    history = [{"role": "system", "content": "You are a helpful assistant."}]
    send_message(client, history, "My order is 4471")
    send_message(client, history, "Thanks, that's all for now.")

    reply = send_message(client, history, "What was my order number?")
    result = "OK"
    if "4471" not in reply:
        result = "WRONG"
    print(f"Case 3 (memory) -> {result}: {reply}")
SAMPLES_PATH = "data/sample/messages.json"

def load_samples() -> dict:
    with open(SAMPLES_PATH) as samples_file:
        return json.loads(samples_file.read())
def test_every_sample_gets_a_ticket(client: OpenAI, samples: dict) -> None:
    for message in samples["triage"]:
        ticket = triage_agent(client, message)
        if ticket is None:
            print("case4 (ticket) WRONG: no ticket")
        else:
            print(f"case 4 (ticket) --> OK , {ticket.issue_category}")
def test_no_invented_name(client: OpenAI, samples: dict) -> None:
    ticket = triage_agent(client, samples["triage"][1])
    result = "OK"
    if ticket is None or ticket.customer_name is not None:
        result = "WRONG"
    print(f"Case 5 (no name) -> {result}")
def test_routing(client: OpenAI, samples: dict) -> None:
    for case in samples["routing"]:
        decision = decide(client, case["message"])
        result = "OK"
        if decision.agent != case["expected"]:
            result = "WRONG"
        print(f"Case 6 (routing) -> {result}: {decision.agent}")
if __name__ == "__main__":
    config = load_config()
    client = create_client(config)
    test_first_reply(client)
    test_bad_key()
    test_memory(client)

    # Step 3
    samples = load_samples()
    test_every_sample_gets_a_ticket(client, samples)
    test_no_invented_name(client, samples)
    # Step 4
    test_routing(client, samples)