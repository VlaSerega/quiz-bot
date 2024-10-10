import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from database.crud import get_user_by_id, update_user
import async_bot.consts as const


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        super().__init__()
        self._sessionmaker = sessionmaker

    async def on_pre_process_message(self, message: types.Message, data: dict):
        logging.info(message.chat.id)
        # await self.open_session_and_get_user(message, data)

    async def on_process_message(self, message: types.Message, data: dict):
        await self.open_session_and_get_user(message, data)

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        await self.open_session_and_get_user(callback.message, data)

    async def on_post_process_message(self, message: types.Message, data_from_filter: list, data: dict):
        await self.close_session(data)

    async def on_post_process_callback_query(self, callback: types.CallbackQuery, data_from_filter: list, data: dict):
        await self.close_session(data)

    async def open_session_and_get_user(self, message, data: dict):
        session = self._sessionmaker()
        data[const.SESSION] = session

        user = await get_user_by_id(message.from_user.id, session)
        data[const.USER] = user

        if user is not None:
            user.username = message.from_user.username
            await update_user(user, session)

    async def close_session(self, data: dict):
        if const.SESSION in data:
            session = data[const.SESSION]

            if session:
                await session.close()
