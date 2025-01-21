from __future__ import annotations

import re

import pymorphy3

from config.constants import ADJECTIVE_TO_COUNTRY, COUNTRIES, KEYWORDS, STOP_WORDS

morph_analyzer = pymorphy3.MorphAnalyzer()


def normalize_word(word: str) -> str:
    """Normalize a word using lemmatization and country mapping."""
    lemma = morph_analyzer.parse(word)[0].normal_form
    return ADJECTIVE_TO_COUNTRY.get(lemma, lemma)


def extract_words(text: str) -> list[str]:
    """Extract words from text using a regular expression."""
    return re.findall(r"[а-яА-ЯёЁ]+", text)


def find_countries_in_words(words: list[str]) -> set[str]:
    """Find distinct countries in a list of words."""
    return {word for word in words if word in COUNTRIES}


def find_keywords_in_words(words: list[str]) -> set[str]:
    """Find keywords in a list of words."""
    return {word for word in words if word in KEYWORDS}


def find_stop_words_in_words(words: list[str]) -> set[str]:
    """Find stop words in a list of words."""
    return {word for word in words if word in STOP_WORDS}
