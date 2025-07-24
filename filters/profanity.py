import re
from aiogram import types
from aiogram.filters import BaseFilter

# Базовый список нецензурных слов (можно расширять)
PROFANITY_LIST = [
    'бля', 'блять', 'сука', 'хуй', 'пизд', 'еба', 'ебл', 'муд', 'гандон', 'чмо', 'сволоч', 'урод', 'долбоёб', 'мудак',
    'сучка', 'шлюха', 'гнида', 'пидор', 'пидр', 'жопа', 'залуп', 'срать', 'ссать', 'гавно', 'говно', 'дерьмо', 'мразь'
]

PROFANITY_REGEX = re.compile(r"|".join([rf"\b{word}\w*\b" for word in PROFANITY_LIST]), re.IGNORECASE)

class ProfanityFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if message.text:
            return bool(PROFANITY_REGEX.search(message.text))
        return False 