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
