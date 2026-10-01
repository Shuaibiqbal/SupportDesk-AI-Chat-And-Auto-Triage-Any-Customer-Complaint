from openai import OpenAI
import openai
def create_client(config) -> OpenAI:
    return OpenAI()

def check_api_key_at_startup(client: OpenAI, max_tokens = 1):
    try:
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"user","content": "Hi"},
            ],
        )
    except openai.AuthenticationError:
        return False
    return True

def send_message(client: OpenAI, history:list[dict]):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages= history,
    )
    return response.choices[0].message.content
def stream_msg(client: OpenAI, history: list[dict]):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        stream=True
    )
    return stream