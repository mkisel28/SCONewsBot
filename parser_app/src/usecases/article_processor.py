import httpx
from newspaper import Article

from config.logging import setup_logging
from domain.models import Feed
from repositories.article_repository import ArticleRepository
from services.deepseek_service import DeepSeekService
from services.telegram_notifier_service import TelegramNotifierService
from services.text_processor_service import TextProcessorService
from utils.http_utils import fetch_url

main_logger, ai_logger = setup_logging()


class ArticleProcessor:
    """UseCase для обработки одной статьи:
    1) Скачать статью
    2) Спарсить
    3) Проверить критерии (стоп-слова, ключевые слова, страны)
    4) Вызвать DeepSeek (analyze + rewrite) при необходимости
    5) Уведомить админов
    """

    def __init__(
        self,
        client: httpx.AsyncClient,
        text_processor: TextProcessorService,
        deepseek_service: DeepSeekService,
        telegram_notifier: TelegramNotifierService,
        article_repository: ArticleRepository,
        parser_config,
    ) -> None:
        """Инициализация UseCase."""
        self._client = client
        self._text_processor = text_processor
        self._deepseek_service = deepseek_service
        self._telegram_notifier = telegram_notifier
        self._article_repository = article_repository
        self._parser_config = parser_config

    async def process_article_link(self, link: str, feed: Feed) -> None:  # noqa C901
        """Обработка одной статьи."""
        is_exists = await self._article_repository.exists_by_link(link)
        if is_exists:
            return

        main_logger.info(f"Processing article: {link}")
        await self._article_repository.create_article(link=link, feed=feed)

        response = await fetch_url(self._client, link)
        if not response:
            return

        article_content = self._parse_article(link, response.text)
        if not article_content or not article_content.get("text"):
            main_logger.error(
                f"Failed to parse article or no content found for {link}",
            )
            return

        text = article_content["text"]

        countries_found = self._process_text(text)
        if not countries_found:
            main_logger.info(
                f"No interesting countries found or stop words exist in {link}",
            )
            return

        is_sco_related = await self._deepseek_service.analyze_with_deepseek(
            text,
        )
        if not is_sco_related:
            main_logger.info(
                f"Article {link} is not SCO related by DeepSeek analysis.",
            )
            return

        await self._article_repository.update_article_texts(
            link=link,
            original_text=text,
        )

        rewrite_text = await self._deepseek_service.rewrite_text_with_deepseek(
            text,
        )
        if not rewrite_text:
            main_logger.info(f"Rewrite result is empty for {link}")
            return

        await self._article_repository.update_article_texts(
            link=link,
            rewritten_text=rewrite_text,
        )

        main_logger.info(
            f"Found countries in {link}: {', '.join(countries_found)}",
        )
        with open("processed_links.txt", "a", encoding="utf-8") as file:
            file.write(
                f"{link} - Countries found: {', '.join(countries_found)}\n",
            )

        message = f"Для статьи {link} найдены страны: {', '.join(countries_found)}\n\n{rewrite_text}"
        await self._telegram_notifier.notify_admins(message)

    def _parse_article(
        self,
        url: str,
        html_content: str,
    ) -> dict[str, str] | None:
        """Парсинг статьи c помощью библиотеки newspaper."""
        try:
            article = Article(
                url,
                language="ru",
                config=self._parser_config,
                ignore_read_more=True,
            )
            article.download(input_html=html_content, ignore_read_more=True)
            article.parse()
            return {
                "title": article.title,
                "text": article.text,
            }
        except Exception as e:
            main_logger.exception(f"Error parsing article {url}: {e}")
            return None

    def _process_text(self, text: str) -> None | set[str]:
        """Обработка текста статьи."""
        words = self._text_processor.extract_words(text)
        lemmatized_words = [
            self._text_processor.normalize_word(w.lower()) for w in words
        ]

        found_stop_words = self._text_processor.find_stop_words_in_words(
            lemmatized_words,
        )
        if found_stop_words:
            return None

        found_countries = self._text_processor.find_countries_in_words(
            lemmatized_words,
        )
        found_keywords = self._text_processor.find_keywords_in_words(
            lemmatized_words,
        )

        if len(found_countries) < 2 or not found_keywords:
            return None

        return found_countries
