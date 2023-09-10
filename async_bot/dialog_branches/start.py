from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from async_bot.dialog_branches.clients.states import FSMGreeting
from async_bot.dialog_branches.utils import create_keyboard_inline, Button, menu_keyboard
from database.crud import update_user
from database.models import User, Team


async def command_start(message: types.Message, session: AsyncSession, user: User):
    if user is None:
        user = User(chat_id=message.chat.id, username=message.chat.username, name=message.chat.first_name)
        await update_user(user, session)

        await FSMGreeting.team.set()
        await message.answer("#ОткрывайАлтай с <b>Мариком</b> и <b>Марей</b>")
        await message.answer("Выбери, с кем ты путешествуешь", reply_markup=create_keyboard_inline(
            [Button('Марик', 'Марик'), Button('Маря', 'Маря')]
        ))
    else:
        await message.answer("#ОткрывайАлтай с <b>Мариком</b> и <b>Марей</b>", reply_markup=menu_keyboard)


async def command_creator(message: types.Message):
    await message.answer("Создатель бота: @VlaSerega.",
                         reply_markup=ReplyKeyboardRemove())


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"], chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(command_creator, commands=['creator'], state="*", chat_type=types.ChatType.PRIVATE)
