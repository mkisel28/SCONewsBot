from __future__ import annotations

import random

import httpx

from config.logging import setup_logging
from utils.decarators import retry_async

main_logger, _ = setup_logging()


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edge/83.0.478.64",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.90",
    "Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
]


def get_random_user_agent() -> str:
    """Возвращает случайный User-Agent из списка."""
    return random.choice(USER_AGENTS)


@retry_async(
    retries=3,
    delay=2.0,
    errors=(
        httpx.RequestError,
        httpx.HTTPStatusError,
        httpx.RemoteProtocolError,
        httpx.TimeoutException,
    ),
    default=None,
    logger=main_logger,
)
async def fetch_url(
    client: httpx.AsyncClient,
    url: str,
) -> httpx.Response | None:
    """Запрашивает URL и возвращает ответ, либо None при неудаче."""
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = await client.get(
        url, timeout=40, follow_redirects=True, headers=headers
    )
    response.raise_for_status()
    return response


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
