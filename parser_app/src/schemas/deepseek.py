
from pydantic import BaseModel


class DeepSeekResult(BaseModel):
    success: bool
    result: bool | None = None
    error: str | None = None
    error_type: str | None = None
