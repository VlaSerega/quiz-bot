from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from async_bot.dialog_branches.clients.states import FSMGreeting
from async_bot.dialog_branches.text_message import OLEN_GREET
from async_bot.dialog_branches.utils import menu_keyboard, Button, create_keyboard_inline
from database.crud import *
from database.models import Team


async def greeting_name(message: types.Message, state: FSMContext):
    await message.answer(
        f"Отлично, <b>{message.text}</b>. Сейчас тебе нужно выбрать верный маршрут твоего путешествия. Первая остановка будет в ... (Если сомневаешся, уточни у экскурсовода)",
        reply_markup=create_keyboard_inline(
            [Button('В полковниково с Мариком', 'Марик'), Button('В Бийске с Марей', 'Маря')]
        ))
    await state.set_state(FSMGreeting.team)


async def greeting_team(callback: types.CallbackQuery, session: AsyncSession, user: User,
                        state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    team = callback.data

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
    dp.callback_query.register(greeting_team, FSMGreeting.team)
