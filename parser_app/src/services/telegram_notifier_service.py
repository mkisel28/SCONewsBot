import asyncio

import httpx

from config.logging import setup_logging
from utils.http_utils import post_request

main_logger, ai_logger = setup_logging()


class TelegramNotifierService:
    """Сервис для отправки уведомлений админам в Telegram."""

    def __init__(self, bot_token: str, admin_ids: list[int]):
        self._bot_token = bot_token
        self._admin_ids = admin_ids

    async def notify_admins(self, message: str):
        """Асинхронная отправка уведомления всем администраторам в Telegram.

        :param message: Текст сообщения, который будет отправлен администраторам.
        """
        url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"

        async with httpx.AsyncClient() as client:
            tasks = []
            for admin_id in self._admin_ids:
                payload = {
                    "chat_id": admin_id,
                    "text": message,
                    "parse_mode": "markdown",
                }
                tasks.append(post_request(client, url, payload))
            await asyncio.gather(*tasks)
