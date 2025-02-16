from tortoise import fields, models


class Country(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)

    class Meta:
        table = "configpanel_country"


class AdjectiveToCountry(models.Model):
    id = fields.IntField(pk=True)
    adjective = fields.CharField(max_length=100, unique=True)
    country = fields.ForeignKeyField(
        "models.Country",
        related_name="adjectives",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "configpanel_adjectivetocountry"


class Keyword(models.Model):
    id = fields.IntField(pk=True)
    word = fields.CharField(max_length=100, unique=True)

    class Meta:
        table = "configpanel_keyword"


class StopWord(models.Model):
    id = fields.IntField(pk=True)
    word = fields.CharField(max_length=100, unique=True)

    class Meta:
        table = "configpanel_stopword"


class Feed(models.Model):
    id = fields.IntField(pk=True)
    feed_url = fields.CharField(max_length=255, unique=True)
    feed_type = fields.CharField(max_length=10, default="rss")
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "configpanel_feed"


class TelegramAdmin(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)

    class Meta:
        table = "configpanel_telegramadmin"


class BotConfig(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, default="DefaultBotConfig")
    token = fields.CharField(max_length=255)

    class Meta:
        table = "configpanel_botconfig"


class NewsArticle(models.Model):
    id = fields.IntField(pk=True)
    feed = fields.ForeignKeyField(
        "models.Feed",
        related_name="news_articles",
        null=True,
        on_delete=fields.SET_NULL,
    )
    link = fields.CharField(max_length=255)
    original_text = fields.TextField(null=True)
    rewritten_text = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "configpanel_newsarticle"


class Prompt(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    prompt_type = fields.CharField(max_length=20)
    content = fields.TextField()
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "configpanel_prompt"
