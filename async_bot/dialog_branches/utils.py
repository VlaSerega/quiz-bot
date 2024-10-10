from collections import namedtuple
import random
from typing import List

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from async_bot.dialog_branches.clients.question import Question, QuestionType

Button = namedtuple("Button", ["name", "data"])


class AnswerCallbackData(CallbackData, prefix='answer'):
    answer_id: int


def create_keyboard_reply(buttons: List[str], rows: List[int] = None) -> ReplyKeyboardMarkup:
    if rows is None:
        rows = [1] * len(buttons)

    if len(buttons) != sum(rows):
        raise Exception(
            f"Bad amount of button. Button: {len(buttons)}, rows: {sum(rows)}"
        )

    keyboard = ReplyKeyboardBuilder()
    new_buttons = [KeyboardButton(text=x) for x in buttons]

    index = 0
    for amount in rows:
        keyboard.row(*new_buttons[index: index + amount])
        index += amount

    return keyboard.as_markup(resize_keyboard=True)


def create_keyboard_inline(buttons: List[Button], rows: List[int] = None) -> InlineKeyboardMarkup:
    if rows is None:
        rows = [1] * len(buttons)

    if len(buttons) != sum(rows):
        raise Exception(
            f"Bad amount of button. Button: {len(buttons)}, rows: {sum(rows)}"
        )

    keyboard = InlineKeyboardBuilder()
    new_buttons = [InlineKeyboardButton(text=x.name, callback_data=x.data) for x in buttons]

    index = 0
    for amount in rows:
        keyboard.row(*new_buttons[index: index + amount])
        index += amount

    return keyboard.as_markup()


async def process_question(message: types.Message, question: Question | List[Question], state: FSMContext,
                           additional_message=None):
    keyboard = ReplyKeyboardRemove()
    if type(question) is list:
        question = random.choice(question)
    answers = question.answers
    text_message = question.body

    if question.type == QuestionType.some:
        buttons = [Button(f"⚪ {a.answer}", AnswerCallbackData(answer_id=i).pack()) for i, a in enumerate(answers)]
        rows = [2 if (i + 1) * 2 <= len(buttons) else 1 for i in range((len(buttons) + 1) // 2)]
        buttons.append(Button('Ответить', 'Ответ'))
        rows.append(1)

        keyboard = create_keyboard_inline(buttons, rows)
    elif question.type == QuestionType.one or question.type == QuestionType.any:
        keyboard = create_keyboard_reply(answers, [len(answers)])
        if additional_message is not None:
            text_message += additional_message

    if question.picture is not None:
        await message.answer_photo(question.picture, caption=text_message,
                                   reply_markup=keyboard)
    else:
        await message.answer(text_message, reply_markup=keyboard)
    if question.state is not None:
        await state.set_state(question.state)
    return question


def message_by_part(text) -> list:
    messages = []
    tmp = ''

    for s in text.split('\n'):
        if len(tmp) + len(s) < 4096:
            tmp += '\n' + s
        else:
            messages.append(tmp)
            tmp = ''
    tmp = tmp.strip()
    if len(tmp) > 2:
        messages.append(tmp)

    return messages


menu_keyboard = create_keyboard_reply(["🚌 Поехали"], rows=[1])
