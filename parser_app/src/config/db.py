import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()


DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("POSTGRES_HOST", "localhost"),
                "port": os.getenv("POSTGRES_PORT", "5432"),
                "user": os.getenv("POSTGRES_USER", "postgress"),
                "password": os.getenv("POSTGRES_PASSWORD", "Maksim2001"),
                "database": os.getenv("POSTGRES_DB", "mydatabase"),
                "schema": "public",
                "minsize": 10,
                "maxsize": 20,
                "max_queries": 100_000,
            },
        },
    },
    "apps": {
        "models": {
            "models": [
                "domain.models",
            ],
            "default_connection": "default",
        },
    },
    "timezone": "UTC",
}


async def init_db() -> None:
    """Инициализация подключения и генерация схем."""
    await Tortoise.init(config=DB_CONFIG)
