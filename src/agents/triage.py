
from openai import OpenAI
from src.schemas import SupportTicket
from src.utils.logger import get_logger
from pydantic import ValidationError
from src.utils.prompts import load_prompt
from src.models.llm import MODEL

def triage_agent(client: OpenAI, message: str) -> SupportTicket | None:
    logger = get_logger(__name__)

    messages = [
        {"role": "system", "content": load_prompt("triage")},
        {"role": "user", "content": message},
    ]

    try:
        completion = client.beta.chat.completions.parse(
            model=MODEL,
            messages=messages,
            response_format= SupportTicket
        )
    except ValidationError as e:
        logger.warning(f"Triage output did not match SupportTicket: {e}")
        return None
    reply = completion.choices[0].message

    if reply.refusal:
        logger.warning(f"Triage agent refused: {reply.refusal}")
        return None
    return reply.parsed