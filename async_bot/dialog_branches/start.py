from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from async_bot.dialog_branches.clients.states import FSMGreeting
from async_bot.dialog_branches.utils import menu_keyboard
from database.crud import update_user
from database.models import User, Team


async def command_start(message: types.Message, session: AsyncSession, user: User):
    if user is None:
        user = User(chat_id=message.chat.id, username=message.chat.username, name=message.chat.first_name)
        await update_user(user, session)

        await FSMGreeting.name.set()
        await message.answer(
            "Привет, я бот #ОткрывайАлтай. Я сделаю твое сегодняшнее путешествие интересней и веселей. А если ты выполнишь все задания - тебя ждет реальный стикер пак с главными Алтайскими маралятами <b>Мариком</b> и <b>Марей</b>.")
        await message.answer("Напиши, как тебя зовут (Имя и фамилия)")
    else:
        await message.answer("#ОткрывайАлтай с <b>Мариком</b> и <b>Марей</b>", reply_markup=menu_keyboard)


async def change_team(message: types.Message, session: AsyncSession, user: User, state: FSMContext):
    if user.team is None:
        await message.answer('Ты пока еще не присоединился ни к одной окманде')
        return

    if user.team == Team.marik:
        user.team = Team.marea
        await message.answer('Теперь ты в команде "Мари"')
    else:
        user.team = Team.marik
        await message.answer('Теперь ты в команде "Марика"')

    await update_user(user, session)
    await state.finish()


async def command_creator(message: types.Message):
    await message.answer("Создатель бота: @VlaSerega.",
                         reply_markup=ReplyKeyboardRemove())


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start"], chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(command_creator, commands=['creator'], state="*", chat_type=types.ChatType.PRIVATE)
    dp.register_message_handler(change_team, commands=['change_team'], state="*", chat_type=types.ChatType.PRIVATE)
