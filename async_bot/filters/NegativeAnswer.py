from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class NegativeAnswer(BoundFilter):
    _negative_phrases = ["нет", "н", "-", "no", "nou", "noy", "ноу", "нет еще", "пока нет", "нет пока", "еще нет", "ни"]

    async def check(self, message: types.Message) -> bool:
        text = message.text

        if text is not None:
            text = text.lower()
            return text in self._negative_phrases

        return False
