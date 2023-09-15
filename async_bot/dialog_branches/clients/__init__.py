from aiogram import Dispatcher

from async_bot.dialog_branches.clients.greeting import register_greeting
from async_bot.dialog_branches.clients.stations import register_stations
from async_bot.dialog_branches.clients.test import register_test


def register_client_handlers(dp: Dispatcher):
    register_greeting(dp)
    register_stations(dp)
    register_test(dp)
