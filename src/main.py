import logging
import httpx
import pymorphy3
import re
import feedparser
import asyncio
from newspaper import Article, Config
from httpx import AsyncClient

logging.basicConfig(
    filename="parser.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

COUNTRIES: list[str] = [
    "россия",
    "беларусь",
    "пакистан",
    "индия",
    "китай",
    "иран",
    "казахстан",
    "таджикистан",
    "киргизия",
    "узбекистан"
]

ADJECTIVE_TO_COUNTRY: dict[str, str] = {
    "российский": "россия",
    "китайский": "китай",
    "белорусский": "беларусь",
    "беларусский": "беларусь",
    "белоруссия": "беларусь",
    "пакистанский": "пакистан",
    "индийский": "индия",
    "иранский": "иран",
    "казахстанский": "казахстан",
    "таджикский": "таджикистан",
    "киргизский": "киргизия",
    "узбекский": "узбекистан",
    "рб": "беларусь",
    "рф": "россия",
    "кнр": "китай",
}

morph_analyzer = pymorphy3.MorphAnalyzer()
config = Config()
config.fetch_images = False

def normalize_word(word: str) -> str:
    """Normalize a word using lemmatization and country mapping."""
    lemma = morph_analyzer.parse(word)[0].normal_form
    return ADJECTIVE_TO_COUNTRY.get(lemma, lemma)

def extract_words(text: str) -> list[str]:
    """Extract words from text using a regular expression."""
    return re.findall(r"[а-яА-ЯёЁ]+", text)

def find_countries_in_words(words: list[str]) -> set[str]:
    """Find distinct countries in a list of words."""
    return {word for word in words if word in COUNTRIES}

async def fetch_url(client: AsyncClient, url: str) -> httpx.Response | None:
    """Fetch a URL and return the response."""
    try:
        response = await client.get(url, timeout=30, follow_redirects=True)
        response.raise_for_status()
        return response
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return None

async def parse_article(url: str, html_content: str) -> dict[str, str] | None:
    """Parse article content using Newspaper4k."""
    try:
        article = Article(url, language="ru", config=config, ignore_read_more=True)
        article.download(input_html=html_content, ignore_read_more=True)
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
        }
    except Exception as e:
        logging.error(f"Error parsing article {url}: {e}")
        return None

async def fetch_rss_links(client: AsyncClient, feed_url: str) -> list[str]:
    """Fetch links from an RSS feed."""
    response = await fetch_url(client, feed_url)
    if response:
        feed = feedparser.parse(response.text)
        return [entry.link for entry in feed.entries if "link" in entry]
    return []

async def process_text(text: str) -> set[str] | None:
    """Process text to find at least two distinct countries."""
    words = extract_words(text)
    lemmatized_words = [normalize_word(word.lower()) for word in words]
    found_countries = find_countries_in_words(lemmatized_words)
    return found_countries if len(found_countries) >= 2 else None

async def process_article_link(link: str, client: AsyncClient, processed_links: set[str]) -> None:
    """Process a single article link."""
    if link in processed_links:
        return

    logging.info(f"Processing article: {link}")
    processed_links.add(link)

    response = await fetch_url(client, link)
    if not response:
        return

    article_content = await parse_article(link, response.text)
    if article_content and article_content.get("text"):
        countries_found = await process_text(article_content["text"])

        if countries_found:
            logging.info(f"Found countries in {link}: {', '.join(countries_found)}")
            with open("processed_links.txt", "a", encoding="utf-8") as file:
                file.write(f"{link} - Countries found: {', '.join(countries_found)}\n")
        else:
            logging.info(f"No countries found in {link}")
    else:
        logging.error(f"Failed to parse article or no content found for {link}")

async def process_links_in_batches(links: list[str], client: AsyncClient, processed_links: set[str], batch_size: int = 20) -> None:
    """Process all links in batches of a specified size."""
    for start in range(0, len(links), batch_size):
        batch = links[start:start + batch_size]
        tasks = [process_article_link(link, client, processed_links) for link in batch]
        await asyncio.gather(*tasks)

async def main() -> None:
    """Main function to process RSS feeds and find countries in articles."""
    rss_feeds: list[str] = [
        "https://tass.ru/rss/v2.xml",
        "https://ria.ru/export/rss2/archive/index.xml",
    ]

    processed_links: set[str] = set()

    async with httpx.AsyncClient() as client:
        for feed_url in rss_feeds:
            logging.info(f"Fetching RSS feed: {feed_url}")
            links = await fetch_rss_links(client, feed_url)
            if not links:
                logging.warning(f"No links found in RSS feed {feed_url}")
                continue

            await process_links_in_batches(links, client, processed_links, batch_size=20)

if __name__ == "__main__":
    asyncio.run(main())
