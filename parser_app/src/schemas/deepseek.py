from pydantic import BaseModel


class DeepSeekResult(BaseModel):
    """Результат анализа текста с помощью DeepSeek."""

    success: bool
    title: str | None = None
    result: bool | None = None
    error: str | None = None
    error_type: str | None = None


class DeepSeekRewriteResult(BaseModel):
    """Результат переформулирования текста с помощью DeepSeek."""

    success: bool
    title: str | None = None
    text: str | None = None
    error: str | None = None
    error_type: str | None = None
