from domain.models import Feed, NewsArticle


class ArticleRepository:
    """Репозиторий для работы с NewsArticle в базе данных."""

    async def exists_by_link(self, link: str) -> bool:
        """Проверяем, есть ли уже в БД статья с таким link."""
        return await NewsArticle.filter(link=link).exists()

    async def create_article(
        self,
        link: str,
        feed: Feed | None = None,
    ) -> NewsArticle:
        """Создаём новую запись в таблице NewsArticle."""
        article = await NewsArticle.create(
            link=link,
            feed=feed,
            original_text=None,
            rewritten_text=None,
        )
        return article

    async def get_or_create_article(
        self,
        link: str,
        feed: Feed | None = None,
    ) -> NewsArticle:
        """Метод "get or create". Если не существует запись с таким link – создаём.
        Если существует – возвращаем.
        """
        article = await NewsArticle.get_or_none(link=link)
        if article is None:
            article = await self.create_article(link=link, feed=feed)
        return article

    async def update_article_texts(
        self,
        link: str,
        *,
        original_text: str | None = None,
        rewritten_text: str | None = None,
    ) -> bool:
        """Метод для обновления как original_text, так и rewritten_text.
        Обновляет только те поля, которые переданы в аргументах.
        """
        article = await NewsArticle.get_or_none(link=link)
        if article:
            if original_text is not None:
                article.original_text = original_text
            if rewritten_text is not None:
                article.rewritten_text = rewritten_text
            await article.save()
            return True
        return False
