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
    msg = "DEEPSEEK_API_KEY is not set in the environment variables"
    raise ValueError(msg)

WORDPRESS_URL = os.getenv("WORDPRESS_URL", "https://scomedia.ru")
WORDPRESS_API_ENDPOINT = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME", "Redaktor")
WORDPRESS_APP_PASSWORD = os.getenv(
    "WORDPRESS_APP_PASSWORD",
    "password",
)
if WORDPRESS_APP_PASSWORD == "password":
    msg = "WORDPRESS_APP_PASSWORD is not set in the environment variables"
    raise ValueError(msg)

PARSER_CONFIG = Config()
PARSER_CONFIG.fetch_images = False
