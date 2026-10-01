from src.config import load_config
from src.models.llm import create_client, send_message, stream_msg, check_api_key_at_startup
from src.utils.logger import get_logger

def main():

    config = load_config()
    logger = get_logger(__name__)
    client = create_client(config)
    api_working = check_api_key_at_startup(client)

    system_msg = {"role":"system","content":"You are a helpful assistant."}

    history = [system_msg]
    if api_working:
        while True:
            user_input = input("User: ")
            if user_input == "/quit":
                break
            history.append({"role":"user", "content": user_input})
            reply = send_message(client, history)
            print(reply)
        
if __name__ == "__main__":
    main()
