from openai import OpenAI
from src.schemas import RouteDecision
from src.utils.logger import get_logger
from src.utils.prompts import load_prompt
from src.models.llm import MODEL
from pydantic import ValidationError

def decide(client: OpenAI, message: str) -> RouteDecision:
    logger = get_logger(__name__)
    messages = [
        {"role": "system", "content": load_prompt("router")},
        {"role": "user", "content": message}
    ]
    decision = RouteDecision(
        agent="concierge", reason="router could not decide."
    )

    try:
        completion = client.beta.chat.completions.parse(
            model= MODEL,
            messages=messages,
            response_format=RouteDecision
        )
        reply = completion.choices[0].message
        if reply.parsed is not None:
            decision = reply.parsed
    except ValidationError as e:
        logger.warning(f"Router output did not match RouteDecision: {e}")
    logger.info(f" routed to {decision.agent} ({decision.reason}): {message}")

    return decision 

    config = load_config()
    client = create_client(config)

