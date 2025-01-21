from __future__ import annotations

import asyncio

import httpx
from httpx import AsyncClient
from newspaper import Article

from ai.deepseek import analyze_with_deepseek
from config.logging import setup_logging
from config.settings import PARSER_CONFIG
from utils.http_utils import fetch_url
from utils.rss_utils import fetch_rss_links
from utils.text_processing import (
    extract_words,
    find_countries_in_words,
    find_keywords_in_words,
    find_stop_words_in_words,
    normalize_word,
)

main_logger, ai_logger = setup_logging()


async def parse_article(url: str, html_content: str) -> dict[str, str] | None:
    """Parse article content using Newspaper4k."""
    try:
        article = Article(
            url,
            language="ru",
            config=PARSER_CONFIG,
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


async def process_text(text: str) -> set[str] | None:
    """Process text to find at least two distinct countries."""
    words = extract_words(text)
    lemmatized_words = [normalize_word(word.lower()) for word in words]

    found_stop_words = find_stop_words_in_words(lemmatized_words)

    if found_stop_words:
        return None

    found_countries = find_countries_in_words(lemmatized_words)
    found_keywords = find_keywords_in_words(lemmatized_words)

    if len(found_countries) < 2 or not found_keywords:
        return None

    if not analyze_with_deepseek(text):
        return None

    return found_countries


async def process_article_link(
    link: str,
    client: AsyncClient,
    processed_links: set[str],
) -> None:
    """Process a single article link."""
    if link in processed_links:
        return

    main_logger.info(f"Processing article: {link}")
    processed_links.add(link)

    response = await fetch_url(client, link)
    if not response:
        return

    article_content = await parse_article(link, response.text)
    if article_content and article_content.get("text"):
        countries_found = await process_text(article_content["text"])

        if countries_found:
            main_logger.info(f"Found countries in {link}: {', '.join(countries_found)}")
            with open("processed_links.txt", "a", encoding="utf-8") as file:
                file.write(f"{link} - Countries found: {', '.join(countries_found)}\n")
        else:
            main_logger.info(f"No countries found in {link}")
    else:
        main_logger.error(f"Failed to parse article or no content found for {link}")


async def process_links_in_batches(
    links: list[str],
    client: AsyncClient,
    processed_links: set[str],
    batch_size: int = 20,
) -> None:
    """Process all links in batches of a specified size."""
    for start in range(0, len(links), batch_size):
        batch = links[start : start + batch_size]
        tasks = [process_article_link(link, client, processed_links) for link in batch]
        await asyncio.gather(*tasks)


async def main() -> None:
    """Main function to process RSS feeds and find countries in articles."""
    rss_feeds: list[str] = [
        "https://tass.ru/rss/v2.xml",
        "https://ria.ru/export/rss2/archive/index.xml",
        "https://www.interfax.ru/rss.asp",
        "https://rg.ru/xml/index.xml",
        "https://belta.by/rss/",
        "https://sputnik.by/export/rss2/archive/index.xml",
    ]

    processed_links: set[str] = set()

    async with httpx.AsyncClient() as client:
        for feed_url in rss_feeds:
            main_logger.info(f"Fetching RSS feed: {feed_url}")
            links = await fetch_rss_links(client, feed_url)
            if not links:
                main_logger.warning(f"No links found in RSS feed {feed_url}")
                continue

            await process_links_in_batches(
                links,
                client,
                processed_links,
                batch_size=5,
            )


if __name__ == "__main__":
    asyncio.run(main())
