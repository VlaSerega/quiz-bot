from aiogram import Dispatcher

from async_bot.filters.NegativeAnswer import NegativeAnswer


def register_filters(dp: Dispatcher):
    dp.bind_filter(NegativeAnswer)
