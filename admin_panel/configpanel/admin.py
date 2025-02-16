from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet

from .models import (
    AdjectiveToCountry,
    BotConfig,
    Country,
    Feed,
    Keyword,
    NewsArticle,
    Prompt,
    StopWord,
    TelegramAdmin,
)


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "prompt_type",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("prompt_type", "is_active")
    search_fields = ("name", "content")


class AdjectiveToCountryInline(admin.TabularInline):
    model = AdjectiveToCountry
    extra = 1
    verbose_name = "Прилагательное"
    verbose_name_plural = "Прилагательные к стране"


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    inlines = [AdjectiveToCountryInline]


@admin.register(AdjectiveToCountry)
class AdjectiveToCountryAdmin(admin.ModelAdmin):
    list_display = ("id", "adjective", "country")
    search_fields = ("adjective", "country__name")
    list_filter = ("country",)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("id", "word")
    search_fields = ("word",)


@admin.register(StopWord)
class StopWordAdmin(admin.ModelAdmin):
    list_display = ("id", "word")
    search_fields = ("word",)


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "feed_url", "feed_type")
    search_fields = ("feed_url",)
    list_filter = ("feed_type", "is_active")
    list_editable = ("is_active",)


@admin.register(TelegramAdmin)
class TelegramAdminAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id")
    search_fields = ("telegram_id",)


@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "token")
    search_fields = ("name",)


class HasTextFilter(admin.SimpleListFilter):
    title = "Наличие текста"
    parameter_name = "has_text"

    def lookups(self, request, model_admin) -> tuple[tuple[str, str]]:
        return (("yes", "Есть текст"),)

    def queryset(self, request, queryset) -> QuerySet[Any]:
        if self.value() == "yes":
            return queryset.filter(
                original_text__isnull=False,
            ) | queryset.filter(rewritten_text__isnull=False)
        return queryset


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "feed", "link", "created_at", "updated_at")
    search_fields = ("link", "feed__feed_url")
    list_filter = (
        HasTextFilter,
        "feed__feed_type",
        "created_at",
    )  # Добавляем кастомный фильтр
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("feed", "link")}),
        ("Тексты", {"fields": ("original_text", "rewritten_text")}),
        ("Даты", {"fields": ("created_at", "updated_at")}),
    )
