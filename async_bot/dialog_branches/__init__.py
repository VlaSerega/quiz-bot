from aiogram import Dispatcher

from async_bot.dialog_branches.clients import register_client_handlers
from async_bot.dialog_branches.start import register_start_handlers


def register_branches(dp: Dispatcher):
    register_start_handlers(dp)
    register_client_handlers(dp)
