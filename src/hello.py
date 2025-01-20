import logging
import requests
from newspaper import Article, Config
import pymorphy3
import re
import feedparser

logging.basicConfig(
    filename='parser.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Список стран
COUNTRIES = [
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

# Маппинг прилагательных и аббревиатур к существительным
ADJECTIVE_TO_NOUN = {
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

morph = pymorphy3.MorphAnalyzer()
config = Config()
config.fetch_images = False

def lemmatize_word(word):
    """Лемматизация с учетом маппинга прилагательных и аббревиатур"""
    lemma = morph.parse(word)[0].normal_form
    return ADJECTIVE_TO_NOUN.get(lemma, lemma)


def parse_with_newspaper4k(url):
    """Парсинг статьи с использованием библиотеки Newspaper"""
    try:
        article = Article(url, language="ru", config=config)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
        }
    except Exception as e:
        logging.error(f"[Newspaper4k] Error processing {url}: {e}")
        return None


def fetch_rss_feed(url):
    """Получение RSS-ленты и извлечение ссылок на новости"""
    try:
        feed = feedparser.parse(url)
        links = []
        for entry in feed.entries:
            if 'link' in entry:
                links.append(entry.link)
        return links
    except Exception as e:
        logging.error(f"Failed to fetch RSS feed from {url}: {e}")
        return []


def normalize_words(text):
    """Нормализация слов в тексте с лемматизацией"""
    words = re.findall(r"[а-яА-ЯёЁ]+", text)
    normalized = []
    for w in words:
        normalized.append(lemmatize_word(w.lower()))
    return normalized


def check_countries_in_text(normalized_words):
    """Проверка наличия хотя бы двух стран из списка в тексте"""
    found = set()
    for w in normalized_words:
        if w in COUNTRIES:
            found.add(w)
    if len(found) >= 2:
        return found
    else:
        return None


def main():
    """Основная функция парсинга"""
    rss_feeds = [
        "https://tass.ru/rss/v2.xml",
        "https://ria.ru/export/rss2/archive/index.xml",
    ]

    processed_links = set()  

    for feed_url in rss_feeds:
        logging.info(f"Processing RSS feed: {feed_url}")
        links = fetch_rss_feed(feed_url)
        if not links:
            logging.warning(f"No links found in RSS feed {feed_url}")
            continue

        for link in links:
            if link in processed_links:
                continue
            logging.info(f"Processing link: {link}")
            processed_links.add(link)

            data = parse_with_newspaper4k(link)
            if data and data.get("text"):
                normalized = normalize_words(data["text"])
                countries_found = check_countries_in_text(normalized)

                if countries_found:
                    logging.info(f"SUCCESS: Found at least 2 different countries in {link}")
                    with open('processed_links.txt', 'a', encoding='utf-8') as file:
                        file.write(f"{link} - Countries found: {', '.join(countries_found)}\n")
                else:
                    logging.info(f"No pair of countries found in {link}")
            else:
                logging.error(f"Failed to parse or empty content for {link}")


if __name__ == "__main__":
    main()
