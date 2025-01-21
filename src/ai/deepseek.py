import json

from openai import OpenAI

from config.logging import setup_logging
from config.settings import DEEPSEEK_API_KEY

main_logger, ai_logger = setup_logging()

deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


sco_analysis_prompt = """
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
"""


def analyze_with_deepseek(text: str) -> bool:
    """Analyze the text using DeepSeek API to determine if it relates to SCO."""
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": sco_analysis_prompt},
            {"role": "user", "content": text},
        ],
        stream=False,
        response_format={"type": "json_object"},
    )
    try:
        result = json.loads(response.choices[0].message.content)
        return result.get("result", False)
    except Exception as e:
        main_logger.exception(f"Error processing text with DeepSeek: {e}")
        return False


notification_prompt = """
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


"""


def rewrite_text_with_deepseek(text: str) -> str:
    """Rewrite the text using DeepSeek API."""
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": notification_prompt},
            {"role": "user", "content": text},
        ],
        stream=False,
        response_format={"type": "json_object"},
    )
    try:

        raw_response = response.choices[0].message.content
        result = json.loads(raw_response)
        return result.get("result", "")

    except Exception as e:
        main_logger.exception(f"Error processing text with DeepSeek: {e}")
        return ""
