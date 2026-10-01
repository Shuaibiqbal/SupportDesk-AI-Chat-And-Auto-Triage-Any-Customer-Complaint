from dotenv import load_dotenv
from dataclasses import dataclass
import os 
from src.exceptions import MissingConfigError

load_dotenv()

@dataclass
class Config:
    openai_api_key: str
    log_level: str

def require_env(key: str) -> str:

    value = os.getenv(key=key)
    if value is None or value == "":
        raise MissingConfigError(f"Value: {value} -> Missing environment value . please check .env")
    return value

def load_config() ->Config:
    openai_api_key = require_env("OPENAI_API_KEY")
    log_level = require_env("LOG_LEVEL")

    return Config(openai_api_key=openai_api_key, log_level=log_level)