import os

from dotenv import load_dotenv
from newspaper import Config

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.net/v1/analyze"
if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY is not set in the environment variables")

PARSER_CONFIG = Config()
PARSER_CONFIG.fetch_images = False
TELEGRAM_BOT_TOKEN = "7588219119:AAFj4XFsXxuHDnbC04jflabWQEITvE8QGB4"
ADMIN_IDS = [1689568914, 428084316]
