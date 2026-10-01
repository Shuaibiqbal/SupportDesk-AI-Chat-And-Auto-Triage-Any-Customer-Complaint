from src.config import load_config, require_env
import os 
from src.exceptions import MissingConfigError

TEST_SETTING = "SUPPORTDESK_TEST_SETTING"

def test_missing_setting() -> None:
    os.environ.pop(TEST_SETTING, None)
    result = "WRONG"

    try:
        require_env(TEST_SETTING)
    except MissingConfigError:
        result = "OK"
    print(f"case 1 (missing_setting tested) -> {result}")
def test_empty_setting() -> None:
    os.environ[TEST_SETTING] = ""
    result = "WRONG"
    try:
        require_env(TEST_SETTING)
    except MissingConfigError:
        result = "OK"
    print(f"Case2 (Empty string tested) -> {result}")
def test_config_loads() -> None:
    os.environ["OPENAI_API_KEY"] = "sk-test-123"
    config = load_config()
    result = "OK"
    print(config)
    print(config.openai_api_key)
    if config.openai_api_key != "sk-test-123":
        result = "WRONG"
    print(f"Case 3 (config loads ) -> {result}")

if __name__ == "__main__":
    test_missing_setting()
    test_empty_setting()
    test_config_loads()
        