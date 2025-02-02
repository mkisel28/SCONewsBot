from domain.models import (
    AdjectiveToCountry,
    BotConfig,
    Country,
    Feed,
    Keyword,
    StopWord,
    TelegramAdmin,
)


class DataRepository:
    """Интерфейс / абстракция для получения всех необходимых данных."""

    async def get_countries(self) -> list[str]:
        raise NotImplementedError

    async def get_adjective_to_country_map(self) -> dict[str, str]:
        raise NotImplementedError

    async def get_keywords(self) -> list[str]:
        raise NotImplementedError

    async def get_stop_words(self) -> list[str]:
        raise NotImplementedError

    async def get_feeds(self) -> list[Feed]:
        raise NotImplementedError

    async def get_admin_ids(self) -> list[int]:
        raise NotImplementedError

    async def get_telegram_bot_token(self) -> str:
        raise NotImplementedError


class DatabaseDataRepository(DataRepository):
    """Реализация репозитория для получения данных из базы посредством Tortoise ORM.

    Методы реализованы асинхронно.
    """

    async def get_countries(self) -> list[str]:
        countries = await Country.all().values_list("name", flat=True)
        return [c if isinstance(c, str) else c[0] for c in countries]

    async def get_adjective_to_country_map(self) -> dict[str, str]:
        records = await AdjectiveToCountry.all().prefetch_related("country")
        return {record.adjective: record.country.name for record in records}

    async def get_keywords(self) -> list[str]:
        keywords = await Keyword.all().values_list("word", flat=True)
        return [k if isinstance(k, str) else k[0] for k in keywords]

    async def get_stop_words(self) -> list[str]:
        stop_words = await StopWord.all().values_list("word", flat=True)
        return [w if isinstance(w, str) else w[0] for w in stop_words]

    async def get_feeds(self) -> list[Feed]:
        for feed in await Feed.all():
            print(feed.feed_url)
        return await Feed.all()

    async def get_admin_ids(self) -> list[int]:
        admin_ids = await TelegramAdmin.all().values_list(
            "telegram_id",
            flat=True,
        )
        return [a if isinstance(a, int) else a[0] for a in admin_ids]

    async def get_telegram_bot_token(self) -> str:
        config = await BotConfig.first()
        return config.token if config else ""
