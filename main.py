import sys
from src.config import load_config
from src.exceptions import MissingConfigError
from src.models.llm import (
 check_api_key_at_startup,
 create_client,
 send_message,
 stream_msg
)
from src.utils.prompts import load_prompt
from src.utils.history import trim_history
from src.utils.logger import get_logger

MAX_HISTORY_TOKEN = 100

def main() -> None:
    try:
        config = load_config()
    except MissingConfigError as e:
        print(f"Setup problem: {e}")
        sys.exit(1)

    logger = get_logger(__name__)
    client = create_client(config)
    if not check_api_key_at_startup(client):
        logger.error("Authentication failed — check OPENAI_API_KEY.")
        print("Login failed — check OPENAI_API_KEY in your .env file.")
        sys.exit(1)
    print("Step1: Send message")
    # logger.info("Sending a test message to the model")
    # history: list[dict] = []
    # reply = send_message(client, history, "What's 2+2?")
    # print(reply)
    print("Step2: history built.")
    history = [{"role": "system", "content": load_prompt("concierge")}]
    while True:
        user_input = input("User: ").strip()
        if user_input == "/quit":
            break
        if user_input == "":
            continue
        trim_history(history, MAX_HISTORY_TOKEN)
        logger.debug(f"Sending {len(history)} earlier messages")
        print()
        print("Assistant: ", end="", flush=True)
        
        stream_msg(client, history, user_input)


if __name__ == "__main__":
    main()