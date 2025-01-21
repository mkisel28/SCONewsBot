from __future__ import annotations

import asyncio

import httpx

from config.logging import setup_logging

main_logger, ai_logger = setup_logging()


async def fetch_url(
    client: httpx.AsyncClient,
    url: str,
    retries: int = 3,
    delay: float = 2.0,
) -> httpx.Response | None:
    """Fetch a URL with retries and return the response."""
    for attempt in range(retries):
        try:
            response = await client.get(url, timeout=30, follow_redirects=True)
            response.raise_for_status()
            return response
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt < retries - 1:
                main_logger.warning(
                    f"Attempt {attempt + 1} failed for URL {url}: {e}. Retrying in {delay} seconds...",
                )
                await asyncio.sleep(delay)
            else:
                main_logger.exception(
                    f"Error fetching URL {url} after {retries} attempts: {e}",
                )
                return None
    return None


async def send_message_with_retry(
    client: httpx.AsyncClient,
    url: str,
    payload: dict,
    retries: int = 3,
    delay: float = 3.0,
) -> bool:
    """Асинхронно отправляет запрос с поддержкой повторных попыток.
    :param url: URL для отправки POST-запроса.
    :param payload: Данные для отправки в теле запроса.
    :param retries: Количество попыток.
    :param delay: Задержка между попытками.
    :return: True, если запрос успешен, иначе False.
    """
    for attempt in range(retries):
        try:
            response = await client.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return True
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            if attempt < retries - 1:
                main_logger.warning(
                    f"Attempt {attempt + 1} failed for URL {url}: {e}. Retrying in {delay} seconds...",
                )
                await asyncio.sleep(delay)
            else:
                main_logger.exception(
                    f"Error fetching URL {url} after {retries} attempts: {e}",
                )
                return False
    main_logger.error(f"All {retries} attempts failed for URL {url}")
    return False
