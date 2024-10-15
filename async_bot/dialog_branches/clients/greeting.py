from aiogram import types, Dispatcher, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from async_bot.dialog_branches.clients.states import FSMGreeting
from async_bot.dialog_branches.text_message import OLEN_GREET
from async_bot.dialog_branches.utils import menu_keyboard, Button, create_keyboard_inline
from database.crud import *
from database.models import Team


class CorrectCallbackData(CallbackData, prefix='is_correct'):
    correct: bool


async def greeting_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        f"Отлично, <b>{message.text}</b>. Напиши, из какой ты школы, можно просто номер", )
    await state.set_state(FSMGreeting.school)


async def greeting_school(message: types.Message, state: FSMContext):
    await state.update_data(school=message.text)
    data = await state.get_data()

    await message.answer(
        f"Проверь, все ли врено:\n- Имя: {data.get('name', '')}\n- Школа: {data.get('school', '')}",
        reply_markup=create_keyboard_inline(
            [Button('Все верно', CorrectCallbackData(correct=True).pack()),
             Button('Не верно', CorrectCallbackData(correct=False).pack())]
        ))
    await state.set_state(FSMGreeting.check)


async def greeting_check_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await callback.message.answer(
        "Сейчас тебе нужно выбрать верный маршрут твоего путешествия. Первая остановка будет в ... (Если сомневаешся, уточни у экскурсовода)",
        reply_markup=create_keyboard_inline(
            [Button('В полковниково с Мариком', 'Марик'), Button('В Бийске с Марей', 'Маря')]
        ))
    await state.set_state(FSMGreeting.team)


async def greeting_check_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    await callback.message.answer("Напиши, как тебя зовут (Имя и фамилия)")

    await state.set_state(FSMGreeting.name)


async def greeting_team(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    data = await state.get_data()

    team = callback.data
    user = User(chat_id=callback.chat.id, username=callback.chat.username, name=data.get('name', ''),
                school=data.get('school', ''))

    if team == 'Марик':
        user.team = Team.marik
        await callback.message.answer_sticker("CAACAgIAAxkBAAPiZPw8yOqJhylJAwoJ5Xket9hNGGYAArQsAAKucNBIdMQwb5fhvYQwBA")
        await callback.message.answer(OLEN_GREET.format('Марик'), reply_markup=menu_keyboard)
    else:
        user.team = Team.marea
        await callback.message.answer_sticker("CAACAgIAAxkBAAPkZPw820nCz5QPVVfoC9OTN7h94mYAAlUtAALkddlINjFgUFvPAAGCMAQ")
        await callback.message.answer(OLEN_GREET.format('Маря'), reply_markup=menu_keyboard)

    await update_user(user, session)
    await state.clear()


def register_greeting(dp: Dispatcher):
    dp.message.register(greeting_name, FSMGreeting.name)
    dp.message.register(greeting_school, FSMGreeting.school)
    dp.callback_query.register(greeting_check_yes, FSMGreeting.check, CorrectCallbackData.filter(F.correct == 'True'))
    dp.callback_query.register(greeting_check_no, FSMGreeting.check, CorrectCallbackData.filter(F.correct == 'False'))
    dp.callback_query.register(greeting_team, FSMGreeting.team)
