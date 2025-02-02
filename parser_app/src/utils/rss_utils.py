from __future__ import annotations

import feedparser
import httpx

from config.logging import setup_logging
from utils.http_utils import fetch_url

main_logger, ai_logger = setup_logging()


async def fetch_rss_links(
    client: httpx.AsyncClient,
    feed_url: str,
) -> list[str]:
    """Fetch links from an RSS feed.

    :return: Список ссылок из RSS-ленты.
    """
    response = await fetch_url(client, feed_url)
    if not response:
        return []

    feed = feedparser.parse(response.text)
    return [
        entry.get("link") or entry.get("guid")
        for entry in feed.entries
        if "link" in entry or "guid" in entry
    ]
