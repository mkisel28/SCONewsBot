import os

from dotenv import load_dotenv
from newspaper import Config

load_dotenv()
DEEPSEEK_API_KEY = os.getenv(
    "DEEPSEEK_API_KEY",
    "sk-a5d5b3ab96b04604aeaf4eb3f4b147d4",
)
DEEPSEEK_API_URL = "https://api.deepseek.net/v1/analyze"
if not DEEPSEEK_API_KEY:
    raise ValueError(
        "DEEPSEEK_API_KEY is not set in the environment variables",
    )

PARSER_CONFIG = Config()
PARSER_CONFIG.fetch_images = False
