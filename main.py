import sys
from src.config import load_config
from src.exceptions import MissingConfigError
import openai
from src.models.llm import (
 check_api_key_at_startup,
 create_client,
 send_message,
 stream_msg
)
from src.agents.triage import triage_agent
from src.utils.prompts import load_prompt
from src.utils.history import trim_history
from src.utils.logger import get_logger
from src.services.desk_service import print_ticket
from src.agents.concierge import start_history
from src.services.desk_service import handle_message

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
    # print("Step1: Send message")
    # logger.info("Sending a test message to the model")
    # history: list[dict] = []
    # reply = send_message(client, history, "What's 2+2?")
    # print(reply)
    # print("Step2: history built.")
    # history = [{"role": "system", "content": load_prompt("concierge")}]
    # while True:
    #     user_input = input("User: ").strip()
    #     if user_input == "/quit":
    #         break
    #     if user_input == "":
    #         continue
    #     trim_history(history, MAX_HISTORY_TOKEN)
    #     logger.debug(f"Sending {len(history)} earlier messages")
    #     print()
    #     print("Assistant: ", end="", flush=True)
        
    #     stream_msg(client, history, user_input)

    # print("Step:3 ")
    # history = [{"role":"system", "content": load_prompt("concierge")}]
    # print("SupportDesk AI — type a message, or /quit to exit.")
    # print("Type /extract <complaint> to file a ticket.")
    # while True:
    #     user_input = input("User: ").strip()

    #     if user_input == "/quit":
    #         break
    #     if user_input == "":
    #         continue
    #     try:
    #         if user_input.startswith("/extract "):
    #             text = user_input.removeprefix("/extract ")
    #             ticket = triage_agent(client, text)
    #             if ticket is None:
    #                 print("Sorry, I could not turn that into a ticket.")
    #             else:
    #                 print(print_ticket(ticket))
    #         else:
    #             trim_history(history, MAX_HISTORY_TOKEN)
    #             print("Assistant: ", end="", flush=True)
    #             stream_msg(client, history, user_input)

    #     except openai.APIConnectionError:
    #         logger.error("API ket stopped working mid-session. ")
    #         print("Login failed - check OPENAI_API_KEY in your .env file.")
    #         sys.exit(1)
    #     except openai.RateLimitError:
    #         logger.warning("Rate limited after the client's retries.")
    #         print("Bus right now - wait a moment and try again.")
    #     except openai.BadRequestError:
    #         logger.warning(f"Request rejected (likely too long): {e}")
    #         if history[-1]["role"] == "user":
    #             history.pop()
    #         print("That message was too long to handle - Please shorten it.")
    #Step 4
    history = start_history()
    print("SupportDesk AI -- type a message, or /quit to exit.")
    while True:
        message = input("User: ").strip()
        if message == "/quit":
            break
        if message == "": continue

        try:
            handle_message(client=client, history=history, message=message)
        except openai.AuthenticationError:
            logger.error("API key stopped working mid session.")
            print("Login failed - check OPENAI_API_KEY in your .env")
            sys.exit(1)
        except openai.RateLimitError:
            logger.warning("Rate limited after the client's retries.")
            print("We are busy right now -wait a moment and try again.")
        except openai.BadRequestError as e:
            logger.warning(f"Request rejected (likely too long): {e}")
            if history[-1]["role"] == "user":
                history.pop()
            print("That message was too long to handle - please shorten it.")

if __name__ == "__main__":
    main()