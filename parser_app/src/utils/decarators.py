import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any


def retry_async(  # noqa: C901
    *,
    retries: int = 3,
    delay: float = 2.0,
    errors: tuple[type[BaseException], ...],
    default: Any = None,
    logger: Any = None,
) -> Callable:
    """Декоратор для повторного вызова асинхронной функции при возникновении указанных ошибок.

    :param retries: Количество попыток (включая первую).
    :param delay: Задержка между попытками в секундах.
    :param errors: Кортеж исключений, при возникновении которых повторяем вызов.
    :param default: Значение, возвращаемое, если все попытки завершились неудачно.
    :param logger: Логгер для записи сообщений.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any | None:  # noqa: C901
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except errors as e:
                    if attempt < retries:
                        if logger:
                            logger.warning(
                                f"Attempt {attempt} failed for {func.__name__} with error: {e}. "
                                f"Retrying in {delay} seconds...",
                            )
                        await asyncio.sleep(delay)
                    else:
                        if logger:
                            logger.exception(
                                f"Final attempt {attempt} failed for {func.__name__} with error: {e}. "
                                f"Returning default value: {default}",
                            )
                        return default
            return None

        return wrapper

    return decorator
