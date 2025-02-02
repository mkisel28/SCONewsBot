from django.db import models


class Country(models.Model):
    """Хранит названия стран."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название страны",
        help_text="Введите название страны (например, Россия, Китай)",
    )

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class AdjectiveToCountry(models.Model):
    """Сопоставление прилагательных и форм (например, 'российский', 'рф') к названию страны."""

    adjective = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Прилагательное/Форма",
        help_text='Введите прилагательное или сокращение, которое соответствует стране (например, "российский", "рф")',
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="adjectives",
        verbose_name="Страна",
        help_text="Выберите страну, к которой относится это прилагательное",
    )

    class Meta:
        verbose_name = "Прилагательное к стране"
        verbose_name_plural = "Прилагательные к странам"

    def __str__(self):
        return f"{self.adjective} → {self.country.name}"


class Keyword(models.Model):
    """Ключевые слова."""

    word = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Ключевое слово",
        help_text='Введите ключевое слово для анализа текста (например, "сотрудничество", "договор")',
    )

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

    def __str__(self):
        return self.word


class StopWord(models.Model):
    """Стоп-слова."""

    word = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Стоп-слово",
        help_text='Введите стоп-слово для фильтрации нежелательных статей (например, "война", "терроризм")',
    )

    class Meta:
        verbose_name = "Стоп-слово"
        verbose_name_plural = "Стоп-слова"

    def __str__(self):
        return self.word


class Feed(models.Model):
    """Модель, описывающая источник: RSS или Sitemap."""

    FEED_TYPE_CHOICES = (
        ("rss", "RSS-лента"),
        ("sitemap", "Sitemap"),
    )
    feed_url = models.URLField(
        unique=True,
        verbose_name="URL источника",
        help_text="Введите URL RSS-ленты или Sitemap",
    )
    feed_type = models.CharField(
        max_length=10,
        choices=FEED_TYPE_CHOICES,
        default="rss",
        verbose_name="Тип источника",
        help_text="Выберите тип источника: RSS или Sitemap",
    )

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"

    def __str__(self):
        return f"{self.feed_url}"


class TelegramAdmin(models.Model):
    """Хранит telegram_id админов, которым будут отправляться уведомления."""

    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name="Telegram ID администратора",
        help_text="Введите Telegram ID администратора, которому будут отправляться уведомления",
    )

    class Meta:
        verbose_name = "Telegram администратор"
        verbose_name_plural = "Telegram администраторы"

    def __str__(self):
        return str(self.telegram_id)


class BotConfig(models.Model):
    """Хранит настройки бота, включая токен."""

    name = models.CharField(
        max_length=50,
        default="DefaultBotConfig",
        verbose_name="Название конфигурации",
        help_text="Введите название конфигурации для бота",
    )
    token = models.CharField(
        max_length=255,
        verbose_name="Токен бота",
        help_text="Введите токен для доступа к Telegram боту",
    )

    class Meta:
        verbose_name = "Конфигурация бота"
        verbose_name_plural = "Конфигурации ботов"

    def __str__(self) -> str:
        return f"BotConfig: {self.name}"


class NewsArticle(models.Model):
    """Хранение статей, которые были спарсены."""

    feed = models.ForeignKey(
        Feed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Источник",
        help_text="Выберите источник, из которого была получена статья",
    )
    link = models.URLField(
        verbose_name="Ссылка на статью",
        help_text="Введите ссылку на оригинальную статью",
        unique=True,
    )
    original_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Оригинальный текст",
        help_text="Оригинальный текст статьи, полученный при парсинге",
    )
    rewritten_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Переписанный текст",
        help_text="Текст статьи, переписанный ИИ",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления статьи в базу данных",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего обновления записи",
    )

    class Meta:
        verbose_name = "Новостная статья"
        verbose_name_plural = "Новостные статьи"

    def __str__(self) -> str:
        return f"Статья с {self.link}"


class Prompt(models.Model):
    """Хранит промпты для взаимодействия с AI-сервисами.
    Типы промптов:
    - analysis: промпт для анализа текста (например, относится ли статья к ШОС)
    - rewrite: промпт для переформулирования текста
    """

    PROMPT_TYPE_CHOICES = (
        ("analysis", "Analysis Prompt"),
        ("rewrite", "Rewrite Prompt"),
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название",
    )
    prompt_type = models.CharField(
        max_length=20,
        choices=PROMPT_TYPE_CHOICES,
        verbose_name="Тип промпта",
        help_text="Выберите тип промпта (анализ или переформулирование)",
    )
    content = models.TextField(
        verbose_name="Текст промпта",
        help_text="Введите текст промпта",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Флаг активности промпта",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Промпт"
        verbose_name_plural = "Промпты"

    def __str__(self) -> str:
        return f"{self.name}"
