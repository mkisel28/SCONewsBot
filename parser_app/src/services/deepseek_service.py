import json

from openai import OpenAI
from tortoise.exceptions import DoesNotExist

from config.logging import setup_logging
from config.settings import DEEPSEEK_API_KEY
from domain.models import Prompt

main_logger, ai_logger = setup_logging()


class DeepSeekService:
    """Сервис для работы с DeepSeek API.

    Отвечает только за взаимодействие с внешним API: анализ и переформулирование.
    """

    def __init__(self):
        self._client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        )

    async def analyze_with_deepseek(self, text: str) -> bool:
        """Анализирует текст с помощью DeepSeek, определяя, относится ли он к ШОС."""
        try:
            analysis_prompt = await self._get_prompt_from_db("analysis")
            response = self._client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": analysis_prompt},
                    {"role": "user", "content": text},
                ],
                stream=False,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)  # type: ignore
            return result.get("result", False)
        except Exception as e:
            main_logger.exception(
                f"Error processing text with DeepSeek (analyze): {e}",
            )
            return False

    async def rewrite_text_with_deepseek(self, text: str) -> str:
        """Переформулирует текст с помощью DeepSeek."""
        try:
            rewrite_prompt = await self._get_prompt_from_db("rewrite")
            response = self._client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": rewrite_prompt},
                    {"role": "user", "content": text},
                ],
                stream=False,
                response_format={"type": "json_object"},
            )
            raw_response = response.choices[0].message.content
            result = json.loads(raw_response)  # type: ignore
            return result.get("result", "")
        except Exception as e:
            main_logger.exception(
                f"Error processing text with DeepSeek (rewrite): {e}",
            )
            return ""

    async def _get_prompt_from_db(self, prompt_type: str) -> str:
        """Загружает активный промпт из базы данных по заданному типу ('analysis' или 'rewrite').

        Если активный промпт не найден, поднимает исключение.
        """
        try:
            prompt = await Prompt.get(prompt_type=prompt_type, is_active=True)
            return prompt.content
        except DoesNotExist:
            main_logger.error(
                f"No active prompt found for type: {prompt_type}",
            )
            raise ValueError(f"No active prompt found for type: {prompt_type}")
