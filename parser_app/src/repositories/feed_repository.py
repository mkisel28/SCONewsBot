from domain.models import Feed


class FeedRepository:
    """Репозиторий для работы с Feed в базе данных."""

    async def get_feed(self, feed_url: str) -> Feed | None:
        """Находит Feed по feed_url.
        Если не найден — создаёт.
        Возвращает объект Feed.
        """
        feed = await Feed.get_or_none(feed_url=feed_url)
        return feed
