import json
from src.agents.triage import triage_agent
from src.config import load_config
from src.models.llm import create_client

SAMPLES_PATH = "data/sample/messages.json"

def main() -> None:
    config = load_config()
    client = create_client(config)
    with open(SAMPLES_PATH) as sample_file:
        samples = json.loads(sample_file.read())

    for message in samples["triage"]:

        print(f"\n Message: ", message)

        ticket = triage_agent(client, message)
        if ticket is None:
            print("No ticket -- the Triage agent couldn't extract one.")
        else:
            print(f"Ticket: {ticket}")
if __name__ == "__main__":
    main()