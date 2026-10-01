from src.utils.history import estimate_token, trim_history

def test_estimate_tokens() -> None:
    history = [
        {"role": "system", "content": "a"*20},
        {"role": "user", "content": "a"*20}
    ]
    result = "OK"
    if estimate_token(history) != 10:
        result = "WRONG"
    print(f"Case 1 (40 characyers = 10) -> {result}")
def test_short_history_untouched() -> None:
    history = [
        {"role":"system", "content": "be nice"},
        {"role":"user", "content": "hi"},
    ]
    trim_history(history, max_token=100)
    result = "OK"
    if len(history) != 2:
        result = "WRONG"
    print(f"Case 2 ( short chat not trimmed) -> {result}")

def test_long_history_trimmed() -> None:
    history = [{"role": "system", "content": "be nice"}]

    for number in range(1,6):
        history.append({"role": "user", "content": str(number) * 400})
    trim_history(history, max_token=250)
    result = "OK"
    if history[0]["role"] != "system":
        result = "WRONG"
    if history[-1]["content"] != "5" * 400:
        result = "WRONG"
    print(f"Case 3 (long chat trimmed) -> {result}")
if __name__ == "__main__":

    test_estimate_tokens()
    test_short_history_untouched()
    test_long_history_trimmed()