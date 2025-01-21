import httpx

from config.logging import setup_logging
from config.settings import ADMIN_IDS, TELEGRAM_BOT_TOKEN
from utils.http_utils import send_message_with_retry

main_logger, ai_logger = setup_logging()


async def notify_admins(message: str):
    """Асинхронно отправляет уведомление всем администраторам в Telegram.
    :param message: Текст сообщения, который будет отправлен администраторам.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    async with httpx.AsyncClient() as client:
        for admin_id in ADMIN_IDS:
            payload = {
                "chat_id": admin_id,
                "text": message,
                "parse_mode": "markdown",
            }
            await send_message_with_retry(client, url, payload)
