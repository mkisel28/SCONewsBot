import json
import re

import httpx

from config.logging import setup_logging
from utils.http_utils import post_request

main_logger, wp_logger = setup_logging()


class WordPressPostService:
    """Сервис для публикации новостей в WordPress через REST API."""

    def __init__(self, wp_url: str, username: str, app_password: str) -> None:
        """Инициализация сервиса публикации в WordPress.

        :param wp_url: URL сайта WordPress (без слэша в конце).
        :param username: Имя пользователя WordPress.
        :param app_password: Пароль приложения (Application Password).
        """
        self._wp_url = wp_url
        self._username = username
        self._app_password = app_password
        self._api_endpoint = f"{wp_url}/wp-json/wp/v2/posts"

    async def create_post(
        self,
        title: str | None,
        content: str,
        category_id: int | None = None,
    ) -> int | None:
        """Создает черновик поста в WordPress.

        :param title: Заголовок поста.
        :param content: Контент поста в Markdown.
        :param category_id: ID категории (опционально).
        :return: ID созданного поста или None в случае ошибки.
        """
        formatted_content = self._convert_markdown_to_html(content)
        payload = {
            "title": title,
            "content": formatted_content,
            "status": "draft" if title is None else "publish",
        }
        if category_id is not None:
            payload["categories"] = json.dumps([category_id])

        async with httpx.AsyncClient(
            auth=(self._username, self._app_password),
        ) as client:
            if await post_request(client, self._api_endpoint, payload):
                wp_logger.info("Пост успешно создан")
            wp_logger.error("Ошибка при создании поста")
            return None

    @staticmethod
    def _convert_markdown_to_html(text: str) -> str:
        """Конвертирует текст с Markdown-стилями в HTML.

        :param text: Текст в Markdown-формате.
        :return: HTML-версия текста.
        """
        text = re.sub(r"\*(.*?)\*", r"<strong>\1</strong>", text)
        text = re.sub(r"_(.*?)_", r"<em>\1</em>", text)
        return re.sub(
            r"\[(.*?)\]\((.*?)\)",
            r'<a href="\2">\1</a>',
            text,
        )
