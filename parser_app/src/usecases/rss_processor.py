# src/usecases/rss_processor.py

import asyncio

import httpx

from config.logging import setup_logging
from domain.models import Feed
from usecases.article_processor import ArticleProcessor
from utils.rss_utils import fetch_rss_links

main_logger, ai_logger = setup_logging()


class RssProcessor:
    """UseCase для работы c RSS-лентами.

    1) Получаем список ссылок из каждой ленты
    2) Обрабатываем их в батчах
    """

    def __init__(
        self,
        client: httpx.AsyncClient,
        article_processor: ArticleProcessor,
        batch_size: int = 5,
    ) -> None:
        """Инициализация UseCase."""
        self._client = client
        self._article_processor = article_processor
        self._batch_size = batch_size

    async def process_feeds(self, feeds: list[Feed]) -> None:
        """Обработка всех RSS-лент."""
        for feed in feeds:
            main_logger.info(f"Fetching RSS feed: {feed.feed_url}")

            links = await fetch_rss_links(self._client, feed.feed_url)
            if not links:
                main_logger.warning(
                    f"No links found in RSS feed {feed.feed_url}",
                )
                continue
            await self._process_links_in_batches(links, feed)

    async def _process_links_in_batches(
        self,
        links: list[str],
        feed: Feed,
    ) -> None:
        """Обработка ссылок в батчах."""
        for start in range(0, len(links), self._batch_size):
            batch = links[start : start + self._batch_size]
            tasks = [
                self._article_processor.process_article_link(link, feed)
                for link in batch
            ]
            await asyncio.gather(*tasks)
