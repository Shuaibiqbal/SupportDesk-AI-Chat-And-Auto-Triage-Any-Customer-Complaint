CHAR_PER_TOKEN = 4

def estimate_token(history: list[dict]) -> int:
    total_chars = 0
    for message in history:
        # print(message)
        total_chars = total_chars + len(message["content"])
    return total_chars // CHAR_PER_TOKEN

def trim_history(history: list[dict], max_token: int) -> list[dict]:
    while estimate_token(history) > max_token and len(history) > 2:
        del history[1]
    return history