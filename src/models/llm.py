from openai import OpenAI
import openai
from src.config import Config
MODEL = "gpt-4o-mini"
def create_client(config: Config) -> OpenAI:
    return OpenAI(api_key=config.openai_api_key)


def check_api_key_at_startup(client: OpenAI) -> bool:
    try:
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"user","content": "ping"},
            ],
            max_tokens=1,
        )
    except openai.AuthenticationError:
        return False
    return True

def send_message(client: OpenAI, history:list[dict], user_input: str) -> str:
    history.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(model=MODEL, messages=history)
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply

def stream_msg(client: OpenAI, history: list[dict], user_input: str) -> str:
    history.append({"role": "user", "content": user_input})

    stream = client.chat.completions.create(
        model=MODEL,
        messages=history,
        stream=True,
    )
    full_reply = ""
    for chunk in stream:
        piece = chunk.choices[0].delta.content 
        if piece:
            full_reply += piece
            print(piece, end="", flush=True)
    print()
    history.append({"role":"assistant","content":full_reply})

    return full_reply