from src.config import load_config
from src.models.llm import check_api_key_at_startup, create_client, send_message
from openai import OpenAI
def test_first_reply(client: OpenAI) -> None:
    reply = send_message(client, [{"role": "user", "content": "What's 2+2?"}])
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

if __name__ == "__main__":
    config = load_config()
    client = create_client(config)
    test_first_reply(client)
    test_bad_key()