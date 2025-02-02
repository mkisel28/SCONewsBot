import re

import pymorphy3

from config.logging import setup_logging

main_logger, ai_logger = setup_logging()


class TextProcessorService:
    """Сервис для обработки текста: лемматизация, поиск ключевых слов, стоп-слов, стран и т.д.

    При инициализации принимает на вход необходимые данные (или DataRepository).
    """

    def __init__(
        self,
        countries: list[str],
        adjective_to_country_map: dict,
        keywords: list[str],
        stop_words: list[str],
    ) -> None:
        """Инициализация сервиса."""
        self._countries = set(countries)
        self._adjective_to_country = adjective_to_country_map
        self._keywords = set(keywords)
        self._stop_words = set(stop_words)

        self._morph_analyzer = pymorphy3.MorphAnalyzer()

    def normalize_word(self, word: str) -> str:
        """Лемматизация слова."""
        lemma = self._morph_analyzer.parse(word)[0].normal_form
        return self._adjective_to_country.get(lemma, lemma)

    def extract_words(self, text: str) -> list[str]:
        """Извлекает слова (только кириллица)"""
        return re.findall(r"[а-яА-ЯёЁ]+", text)

    def find_countries_in_words(self, words: list[str]) -> set[str]:
        """Находит страны в списке слов."""
        return {w for w in words if w in self._countries}

    def find_keywords_in_words(self, words: list[str]) -> set[str]:
        """Находит ключевые слова."""
        return {w for w in words if w in self._keywords}

    def find_stop_words_in_words(self, words: list[str]) -> set[str]:
        """Находит стоп-слова."""
        return {w for w in words if w in self._stop_words}
