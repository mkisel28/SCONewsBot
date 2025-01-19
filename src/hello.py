import logging
import requests
from xml.etree import ElementTree
from newspaper import Article
import pymorphy3
import re


logging.basicConfig(
    filename='parser.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

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

morph = pymorphy3.MorphAnalyzer()


def parse_with_newspaper4k(url):
    try:
        article = Article(url, language="ru")
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "summary": article.summary,
            "keywords": article.keywords,
        }
    except Exception as e:
        logging.error(f"[Newspaper4k] Error processing {url}: {e}")
        return None


def fetch_sitemaps(base_url):
    sitemaps = []
    try:
        if not base_url.startswith("http"):
            base_url = "https://" + base_url

        robots_url = base_url.rstrip('/') + "/robots.txt"
        resp = requests.get(robots_url, timeout=10)
        if resp.status_code == 200:
            for line in resp.text.splitlines():
                line = line.strip().lower()
                if line.startswith("sitemap:"):
                    sitemap_url = line.split("sitemap:")[1].strip()
                    sitemaps.append(sitemap_url)
        else:
            logging.warning(f"Robots.txt not found or unavailable for {base_url}")
    except Exception as e:
        logging.error(f"Failed to fetch sitemaps from {base_url}: {e}")
    return sitemaps


def extract_links_from_sitemap(sitemap_url, max_links=5):
    """Возвращает первые max_links ссылок на страницы (не вложенные sitemaps)."""
    links = []
    try:
        resp = requests.get(sitemap_url, timeout=10)
        root = ElementTree.fromstring(resp.content)

        # Если встречаем <sitemapindex>, ищем вложенные <sitemap> -> <loc>
        if root.tag.endswith("sitemapindex"):
            for sm in root.findall("{*}sitemap"):
                loc = sm.find("{*}loc")
                if loc is not None:
                    # Рекурсивно обходим вложенные sitemaps
                    sub_links = extract_links_from_sitemap(loc.text, max_links)
                    links.extend(sub_links)
                if len(links) >= max_links:
                    break

        elif root.tag.endswith("urlset"):
            for url_el in root.findall("{*}url"):
                loc = url_el.find("{*}loc")
                if loc is not None:
                    # Простейша эвристика: считаем "новостными" ссылки с /news/ или /articles/
                    if "/news/" in loc.text or "/article" in loc.text:
                        links.append(loc.text)
                    else:
                        # Если нет явного упоминания, всё равно добавим, пока нет чёткого критерия
                        links.append(loc.text)
                if len(links) >= max_links:
                    break

    except Exception as e:
        logging.error(f"Error parsing sitemap {sitemap_url}: {e}")
    return links


def normalize_words(text):
    words = re.findall(r"[а-яА-ЯёЁ]+", text)
    normalized = []
    for w in words:
        p = morph.parse(w.lower())[0]
        normalized.append(p.normal_form)
    return normalized


def check_countries_in_text(normalized_words):
    found = set()
    for w in normalized_words:
        if w in COUNTRIES:
            found.add(w)
        if len(found) >= 2:  
            break
    return len(found) >= 2


def main():
    sites = [
        "tass.ru",
        "ria.ru",
        "interfax.ru",
        "rg.ru",
        "belta.by",
        "sputnik.by",
        "sb.by",
        "mfa.gov.cn/rus",
        "fmprc.gov.cn/rus",
        "russian.news.cn",
        "russian.people.com.cn",
        "tengrinews.kz",
        "informburo.kz",
        "russian.eurasianet.org",
        "kzaif.kz",
        "kaztag.kz/ru/news/",
        "primeminister.kz/ru",
        "www.nur.kz",
        "dknews.kz",
        "economy.gov.ru",
        "mid.ru",
        "government.ru",
        "kremlin.ru"
    ]

    for site in sites:
        logging.info(f"Processing site: {site}")
        sitemaps = fetch_sitemaps(site)
        if not sitemaps:
            logging.warning(f"No sitemaps found for {site}")
            continue

        collected_links = []
        for sm in sitemaps:
            collected_links.extend(extract_links_from_sitemap(sm, max_links=5))
            if len(collected_links) >= 5:
                break

        if not collected_links:
            logging.warning(f"No links extracted from {site}")
            continue

        for link in collected_links[:5]:
            data = parse_with_newspaper4k(link)
            if data and data.get("text"):
                normalized = normalize_words(data["text"])
                if check_countries_in_text(normalized):
                    logging.info(f"SUCCESS: Found at least 2 different countries in {link}")
                else:
                    logging.info(f"No pair of countries found in {link}")
            else:
                logging.error(f"Failed to parse or empty content for {link}")


if __name__ == "__main__":
    main()