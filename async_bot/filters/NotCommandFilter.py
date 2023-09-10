import re

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class NotCommandFilter(BoundFilter):
    _not_command_regexp = r'^[/][.]*'

    async def check(self, message: types.Message) -> bool:
        text = message.text

        if text is not None:
            return False if re.match(self._not_command_regexp, text) else True

        return True
