from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

COUNTRIES = [
    "россия",
    "беларусь",
    "пакистан",
    "индия",
    "китай",
    "иран",
    "казахстан",
    "таджикистан",
    "киргизия",
    "узбекистан",
]

ADJECTIVE_TO_NOUN = {
    "российский": "россия",
    "китайский": "китай",
    "белорусский": "беларусь",
    "беларусский": "беларусь",
    "белоруссия": "беларусь",
    "пакистанский": "пакистан",
    "индийский": "индия",
    "иранский": "иран",
    "казахстанский": "казахстан",
    "таджикский": "таджикистан",
    "киргизский": "киргизия",
    "узбекский": "узбекистан",
    "рб": "беларусь",
    "рф": "россия",
    "кнр": "китай",
}


def lemmatize_word(word):
    lemma = morph.parse(word)[0].normal_form
    return ADJECTIVE_TO_NOUN.get(lemma, lemma)


def find_countries_in_text(text):
    words = text.lower().split()
    lemmatized_words = [lemmatize_word(word) for word in words]

    return [
        country for country in COUNTRIES if lemmatize_word(country) in lemmatized_words
    ]
