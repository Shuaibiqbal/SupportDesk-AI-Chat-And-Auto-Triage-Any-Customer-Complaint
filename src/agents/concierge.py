from openai import OpenAI
from src.utils.history import trim_history
from src.models.llm import stream_msg
from src.utils.prompts import load_prompt


MAX_HISTORY_TOKENS = 300
def start_history() -> list[dict]:
    system_prompt = load_prompt("concierge")
    return [{"role": "system", "content": system_prompt}]
def concierge_agent(client: OpenAI, history: list[dict], message: str): 
    trim_history(history=history, max_token=MAX_HISTORY_TOKENS)    
    return stream_msg(client=client, history=history, user_input=message)