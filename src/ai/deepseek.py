import json

from openai import OpenAI

from config.logging import setup_logging
from config.settings import DEEPSEEK_API_KEY

main_logger, ai_logger = setup_logging()

deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")


system_prompt = """
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
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        stream=False,
        response_format={"type": "json_object"},
    )
    try:
        result = json.loads(response.choices[0].message.content)
        ai_logger.info(f"DeepSeek response: {result} for text: {text}")
        return result.get("result", False)

    except Exception as e:
        main_logger.exception(f"Error processing text with DeepSeek: {e}")
        return False
