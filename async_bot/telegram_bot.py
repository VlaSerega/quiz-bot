import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from dotenv import load_dotenv

from async_bot.dialog_branches import register_branches
from async_bot.dialog_branches.utils import menu_keyboard
from async_bot.middleware import DbSessionMiddleware, ErrorHandlerMiddleware

load_dotenv()

token = "6450954921:AAF12gfmfuX_WiFufcuZeDvcq1Zk07TI0Mk"


async def photo_id(message: types.Message):
    if message.content_type == types.ContentType.PHOTO:
        await message.answer(message.photo[-1].file_id)
    if message.content_type == types.ContentType.STICKER:
        await message.answer(message.sticker.file_id)


async def default(message: types.Message):
    await message.answer_photo("AgACAgIAAxkBAAM0ZPceqsvXX_SgyfABqu-_F4rK4akAAhbLMRu2s7hLIYDF7GgoZewBAAMCAAN5AAMwBA",
                               caption="К сожалению, я еще не умею отвечать на такое.\n\n"
                                       "Возможно, мое меню тебе поможет тебе разобраться",
                               reply_markup=menu_keyboard)


class AsyncBot:

    def __init__(self, sessionmaker):
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode='HTML'))
        self._dp: Dispatcher = Dispatcher(bot=self.bot, storage=MemoryStorage())

        self._dp.update.outer_middleware(ErrorHandlerMiddleware())

        self._dp.message.middleware(DbSessionMiddleware(sessionmaker))
        self._dp.callback_query.middleware(DbSessionMiddleware(sessionmaker))

        logging.basicConfig(
            filename="log.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

    async def start(self):
        register_branches(self._dp)
        # self._dp.register_message_handler(photo_id, state='*', chat_type=types.ChatType.all(),
        #                                   content_types=types.ContentType.all())
        self._dp.message.register(default)

        await self._set_commands()

        try:
            await self._dp.start_polling(self.bot, skip_updates=True)
        finally:
            await self._dp.storage.close()
            await self.bot.session.close()

    async def _set_commands(self):
        commands = [BotCommand(command='change_team', description='Сменить команду'),
                    BotCommand(command='legend', description='Легенда о маралах')]

        await self.bot.set_my_commands(commands, scope=BotCommandScopeDefault())
