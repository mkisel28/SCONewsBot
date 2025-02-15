import asyncio

import httpx

from config.db import init_db
from config.settings import (
    PARSER_CONFIG,
    WORDPRESS_APP_PASSWORD,
    WORDPRESS_URL,
    WORDPRESS_USERNAME,
)
from repositories.article_repository import ArticleRepository
from repositories.data_repository import DatabaseDataRepository
from services.deepseek_service import DeepSeekService
from services.telegram_notifier_service import TelegramNotifierService
from services.text_processor_service import TextProcessorService
from services.wordpress_sender_service import WordPressPostService
from usecases.article_processor import ArticleProcessor
from usecases.rss_processor import RssProcessor


async def process() -> None:
    data_repo = DatabaseDataRepository()
    feed_urls = await data_repo.get_feeds()
    deepseek_service = DeepSeekService()
    text_processor = TextProcessorService(
        countries=await data_repo.get_countries(),
        adjective_to_country_map=await data_repo.get_adjective_to_country_map(),
        keywords=await data_repo.get_keywords(),
        stop_words=await data_repo.get_stop_words(),
    )
    telegram_notifier = TelegramNotifierService(
        bot_token=await data_repo.get_telegram_bot_token(),
        admin_ids=await data_repo.get_admin_ids(),
    )
    wordpress_sender = WordPressPostService(
        wp_url=WORDPRESS_URL,
        username=WORDPRESS_USERNAME,
        app_password=WORDPRESS_APP_PASSWORD,
    )
    article_repository = ArticleRepository()

    async with httpx.AsyncClient() as client:
        article_processor = ArticleProcessor(
            client=client,
            text_processor=text_processor,
            deepseek_service=deepseek_service,
            telegram_notifier=telegram_notifier,
            wordpress_sender=wordpress_sender,
            article_repository=article_repository,
            parser_config=PARSER_CONFIG,
        )

        rss_processor = RssProcessor(client, article_processor, batch_size=5)

        feed_urls = await data_repo.get_feeds()

        await rss_processor.process_feeds(feed_urls)


async def main() -> None:
    await init_db()

    while True:
        try:
            await process()
            await asyncio.sleep(60)
        except Exception:
            await asyncio.sleep(120)


if __name__ == "__main__":
    asyncio.run(main())
