from __future__ import annotations

import httpx

from config.logging import setup_logging
from utils.decarators import retry_async

main_logger, _ = setup_logging()


@retry_async(
    retries=3,
    delay=2.0,
    errors=(httpx.RequestError, httpx.HTTPStatusError),
    default=None,
    logger=main_logger,
)
async def fetch_url(
    client: httpx.AsyncClient,
    url: str,
) -> httpx.Response | None:
    """Запрашивает URL и возвращает ответ, либо None при неудаче."""
    response = await client.get(url, timeout=30, follow_redirects=True)
    response.raise_for_status()
    return response


@retry_async(
    retries=3,
    delay=3.0,
    errors=(httpx.RequestError, httpx.HTTPStatusError),
    default=False,
    logger=main_logger,
)
async def post_request(
    client: httpx.AsyncClient,
    url: str,
    payload: dict,
) -> bool:
    """Отправляет POST-запрос c повторными попытками.

    :param client: Асинхронный HTTP клиент.
    :param url: URL для запроса.
    :param payload: Данные запроса.
    :return: True, если запрос успешен, иначе False.
    """
    response = await client.post(url, json=payload, timeout=60)
    response.raise_for_status()
    return True
