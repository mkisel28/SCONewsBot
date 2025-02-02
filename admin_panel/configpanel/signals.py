from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import (
    AdjectiveToCountry,
    BotConfig,
    Country,
    Feed,
    Keyword,
    StopWord,
    TelegramAdmin,
)

INIT_COUNTRIES = [
    "россия",
    "беларусь",
    "пакистан",
    "индия",
    "китай",
    "иран",
    "казахстан",
    "таджикистан",
    "киргизия",
    "узбекистан",
]
INIT_ADJECTIVE_TO_COUNTRY = {
    "российский": "россия",
    "рф": "россия",
    "москва": "россия",
    "московский": "россия",
    "китайский": "китай",
    "кнр": "китай",
    "пекин": "китай",
    "пекинский": "китай",
    "белорусский": "беларусь",
    "беларусский": "беларусь",
    "белоруссия": "беларусь",
    "белорусия": "беларусь",
    "минск": "беларусь",
    "минский": "беларусь",
    "рб": "беларусь",
    "пакистанский": "пакистан",
    "индийский": "индия",
    "иранский": "иран",
    "казахстанский": "казахстан",
    "таджикский": "таджикистан",
    "киргизский": "киргизия",
    "кыргызстан": "киргизия",
    "кыргызский": "киргизия",
    "кыргыз": "киргизия",
    "узбекский": "узбекистан",
}
INIT_KEYWORDS = [
    "сотрудничество",
    "обмен",
    "договор",
    "поставка",
    "производство",
    "заключить",
    "инвестиция",
    "экономика",
    "торговля",
    "экспорт",
    "импорт",
    "совещание",
    "форум",
    "встреча",
    "подписание",
    "перспектива",
    "развитие",
    "анализ",
    "обсуждение",
    "совместный",
    "инициатива",
    "содействие",
    "стратегия",
    "региональный",
    "взаимосвязанность",
    "интеграция",
    "услуга",
    "проект",
    "транспорт",
]
INIT_STOP_WORDS = [
    "похищение",
    "бомбардировка",
    "переворот",
    "мошенничество",
    "гранатомёт",
    "армия",
    "сепаратизм",
    "танк",
    "десант",
    "грабёж",
    "экстремизм",
    "оборона",
    "преступление",
    "импичмент",
    "пикет",
    "беженец",
    "изнасилование",
    "конфликт",
    "разбой",
    "шантаж",
    "бригада",
    "революция",
    "коррупция",
    "нападение",
    "насилие",
    "днр",
    "снаряжение",
    "пленный",
    "террорист",
    "иммиграция",
    "депортация",
    "диверсия",
    "боевой",
    "бунт",
    "вторжение",
    "спецоперация",
    "фронт",
    "убить",
    "штурм",
    "пехота",
    "оккупация",
    "экстримизм",
    "взрыв",
    "заложник",
    "эмиграция",
    "мигрант",
    "зсу",
    "убийство",
    "пво",
    "боевик",
    "война",
    "протест",
    "кража",
    "всу",
    "цензура",
    "шторм",
    "миномёт",
    "забастовка",
    "повстанец",
    "вс",
    "шпионаж",
    "военный",
    "снаряд",
    "лнр",
    "интервенция",
    "диктатура",
    "аэродром",
    "взятка",
    "митинг",
    "освободить",
    "угон",
    "полиция",
    "мобилизация",
    "репрессия",
    "стрельба",
    "свд",
    "обстрел",
    "терроризм",
    "лоббизм",
    "ракета",
    "артиллерия",
    "авиация",
]
INIT_FEEDS = [
    ("https://tass.ru/rss/v2.xml", "rss"),
    ("https://ria.ru/export/rss2/archive/index.xml", "rss"),
    ("https://www.interfax.ru/rss.asp", "rss"),
    ("https://rg.ru/xml/index.xml", "rss"),
    ("https://belta.by/rss/", "rss"),
    ("https://sputnik.by/export/rss2/archive/index.xml", "rss"),
    ("https://mid.ru/ru/rss.php", "rss"),
    ("https://russian.news.cn/ewjkxml.xml", "rss"),
    ("https://kzaif.kz/rss/all.php", "rss"),
    ("https://www.chinadaily.com.cn/rss/world_rss.xml", "rss"),
    ("http://www.xinhuanet.com/english/rss/worldrss.xml", "rss"),
    ("https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru", "rss"),
    ("https://www.cgtn.com/subscribe/rss/section/world.xml", "rss"),
    ("https://www.cgtn.com/subscribe/rss/section/china.xml", "rss"),
    (
        "https://news.google.com/rss/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRFEzYkdvU0FuSjFLQUFQAQ?hl=ru&gl=RU&ceid=RU%3Aru&oc=11",
        "rss",
    ),
    (
        "https://news.google.com/rss/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNREV6ZHpJM0VnSnlkU2dBUAE?hl=ru&gl=RU&ceid=RU%3Aru",
        "rss",
    ),
]
INIT_TELEGRAM_ADMINS = [1689568914]
INIT_BOT_TOKEN = "7588219119:AAFj4XFsXxuHDnbC04jflabWQEITvE8QGB4"


from .models import Prompt

# Промпты для автозаполнения
INIT_PROMPTS = [
    {
        "name": "SCO Analysis Prompt",
        "prompt_type": "analysis",
        "content": """
отвечай строго в json формате 

все что ты должен делать это либо соглашаться либо нет

Относится это статья к ШОС?
смотря мне интересно любые связи которые могут быть сделаны в рамках ШОС, сотрудничества двух стран.
ключевой задачей ШОС, созданной прежде всего для укрепления взаимного доверия и добрососедства между странами-участницами, было поддержание мира, безопасности и стабильности в регионе Центральной Азии, то сейчас речь идет о глобальном международном политическом и экономическом сотрудничестве стран-участниц ШОС.
Список стран которые меня интересуют:

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

EXAMPLE JSON OUTPUT:
{ 
    "result": true
}
или 
{ 
    "result": false
}
""",
    },
    {
        "name": "News Rewrite Prompt",
        "prompt_type": "rewrite",
        "content": """
Ответь строго в формате JSON, как требует JSON-спецификация.

Цели и задачи:

Переписывать новостные тексты для другого новостного сайта. 
Использовать оформление как для новостной статьи.
Также соблюдать уникальность и SEO оптимизацию. 
Сохранять риторику, стиль и "мысли" автора.
Использовать заголовки и подзаголовки.
не сохранять гиперссылки в тексте.
Не использовать CamelCase.


Процесс работы:

Читать предоставленный текст.
Определять основную идею и ключевые моменты.
Переписывать текст, сохраняя оригинальный стиль и риторику.
Проверять наличие гиперссылок и НЕ сохранять их.
Добавлять заголовки и подзаголовки для удобства чтения. (Колличество подзаголовков до 3 штук)
Используй markdown для форматирования текста:  *заголовок*, _курсив_, *подзаголовок*.

ограничение:
1000-1500 символов
используй вместо " кавычек в тексте который ты переписываешь такие « »

EXAMPLE JSON OUTPUT:
{
    "result": ...
}
""",
    },
]


@receiver(post_migrate)
def populate_initial_data(sender, **kwargs):
    """Заполняем данные только в том случае,
    если наш app_name совпадает с текущим приложением (configpanel).
    """
    if sender.name != "configpanel":
        return

    if not Prompt.objects.exists():
        for prompt_data in INIT_PROMPTS:
            Prompt.objects.create(
                name=prompt_data["name"],
                prompt_type=prompt_data["prompt_type"],
                content=prompt_data["content"],
            )

    if not Country.objects.exists():
        for country_name in INIT_COUNTRIES:
            Country.objects.create(name=country_name)

    if not AdjectiveToCountry.objects.exists():
        countries_dict = {c.name: c for c in Country.objects.all()}
        for adjective, country_name in INIT_ADJECTIVE_TO_COUNTRY.items():
            country_obj = countries_dict.get(country_name)
            if country_obj:
                AdjectiveToCountry.objects.create(
                    adjective=adjective,
                    country=country_obj,
                )

    if not Keyword.objects.exists():
        for w in INIT_KEYWORDS:
            Keyword.objects.create(word=w)

    if not StopWord.objects.exists():
        for w in INIT_STOP_WORDS:
            StopWord.objects.create(word=w)

    if not Feed.objects.exists():
        for feed_url, feed_type in INIT_FEEDS:
            Feed.objects.create(feed_url=feed_url, feed_type=feed_type)

    if not TelegramAdmin.objects.exists():
        for admin_id in INIT_TELEGRAM_ADMINS:
            TelegramAdmin.objects.create(telegram_id=admin_id)

    if not BotConfig.objects.exists():
        BotConfig.objects.create(name="DefaultBotConfig", token=INIT_BOT_TOKEN)
