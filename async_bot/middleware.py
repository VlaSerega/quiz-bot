import logging
import traceback
from typing import Dict, Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import UserContextMiddleware
from aiogram.types import TelegramObject, Update, Message, CallbackQuery

from async_bot.dialog_branches.utils import message_by_part
from database.crud import get_user_by_id, update_user

CHANNEL_ID = -1002148833317
ADMIN_ID = 462939793


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:
            logging.error(traceback.format_exc())
            event_context = UserContextMiddleware.resolve_event_context(event=event)

            if event_context.user is not None:
                await event.bot.send_message(ADMIN_ID, str(event_context.user))

            for m in message_by_part(traceback.format_exc()):
                await event.bot.send_message(ADMIN_ID, m, parse_mode=None)
            return


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        super().__init__()
        self._sessionmaker = sessionmaker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        session = self._sessionmaker()
        data["session"] = session

        user = await get_user_by_id(event.from_user.id, session)
        data["user"] = user

        if user is not None:
            user.username = event.from_user.username
            await update_user(user, session)

        result = await handler(event, data)

        await session.close()

        return result
