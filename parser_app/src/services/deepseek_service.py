import json

from openai import OpenAI
from tortoise.exceptions import DoesNotExist

from config.logging import setup_logging
from config.settings import DEEPSEEK_API_KEY
from domain.models import Prompt
from schemas.deepseek import DeepSeekResult, DeepSeekRewriteResult

main_logger, ai_logger = setup_logging()


class DeepSeekService:
    """Сервис для работы c DeepSeek API.

    Отвечает только за взаимодействие c внешним API: анализ и переформулирование.
    """

    def __init__(self) -> None:
        self._client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        )

    async def analyze_with_deepseek(self, text: str) -> DeepSeekResult:
        """Анализирует текст c помощью DeepSeek, определяя, относится ли он к ШОС."""
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
            return DeepSeekResult(
                success=True,
                result=result.get("result", False),
            )
        except Exception as e:
            main_logger.exception(
                f"Error processing text with DeepSeek (analyze): {e}",
            )
            return DeepSeekResult(
                success=False,
                error=str(e),
                error_type=type(e).__name__,
            )

    async def rewrite_text_with_deepseek(
        self,
        text: str,
    ) -> DeepSeekRewriteResult:
        """Переформулирует текст c помощью DeepSeek."""
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
            return DeepSeekRewriteResult(
                success=True,
                result=result.get("result", ""),
                title=result.get("title", ""),
            )
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
        except DoesNotExist:
            main_logger.error(
                f"No active prompt found for type: {prompt_type}",
            )
            raise ValueError(f"No active prompt found for type: {prompt_type}")
        return prompt.content
