from collections import namedtuple
import random
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from async_bot.dialog_branches.clients.question import Question, QuestionType

Button = namedtuple("Button", ["name", "data"])

callback_data_leave_order = CallbackData("leave_order", "answer")
callback_data_station = CallbackData("station", "id")
callback_data_answer = CallbackData("answer", "answer_id")
callback_data_apply = CallbackData("apply", "answer")


def create_keyboard_reply(buttons: List[str], rows: List[int] = None) -> ReplyKeyboardMarkup:
    if rows is None:
        rows = [1] * len(buttons)

    if len(buttons) != sum(rows):
        raise Exception(
            f"Bad amount of button. Button: {len(buttons)}, rows: {sum(rows)}"
        )

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    new_buttons = [KeyboardButton(x) for x in buttons]

    index = 0
    for amount in rows:
        keyboard.row(*new_buttons[index: index + amount])
        index += amount

    return keyboard


def create_keyboard_inline(buttons: List[Button], rows: List[int] = None) -> InlineKeyboardMarkup:
    if rows is None:
        rows = [1] * len(buttons)

    if len(buttons) != sum(rows):
        raise Exception(
            f"Bad amount of button. Button: {len(buttons)}, rows: {sum(rows)}"
        )

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    new_buttons = [InlineKeyboardButton(x.name, callback_data=x.data) for x in buttons]

    index = 0
    for amount in rows:
        keyboard.row(*new_buttons[index: index + amount])
        index += amount

    return keyboard


async def process_question(message: types.Message, question: Question | List[Question], additional_message=None):
    keyboard = ReplyKeyboardRemove()
    if type(question) is list:
        question = random.choice(question)
    answers = question.answers

    if question.type == QuestionType.some:
        buttons = [Button(f"⚪ {a.answer}", callback_data_answer.new(answer_id=i)) for i, a in enumerate(answers)]
        rows = [2 if (i + 1) * 2 <= len(buttons) else 1 for i in range((len(buttons) + 1) // 2)]
        buttons.append(Button('Ответить', 'Ответ'))
        rows.append(1)

        keyboard = create_keyboard_inline(buttons, rows)
    elif question.type == QuestionType.one or question.type == QuestionType.any:
        keyboard = create_keyboard_reply(answers, [len(answers)])
    text_message = question.body
    if additional_message is not None:
        text_message += additional_message
    if question.picture is not None:
        await message.answer_photo(question.picture, caption=text_message,
                                   reply_markup=keyboard)
    else:
        await message.answer(text_message, reply_markup=keyboard)
    if question.state is not None:
        await question.state.set()
    return question


async def process_remain_question(message: types.Message, remain: list, state: FSMContext, session):
    if len(remain) == 0:
        await state.finish()
        await message.answer('Поздравляю, ты завершил эту станцию!')
    else:
        question = remain.pop()
        await process_question(message, question, session)
        await state.update_data(remain_questions=remain)


def format_text_with_entities(text, entities, as_html=True):
    if text is None:
        return None

    # Create a message object to access the parse_entities method
    message = types.Message(text=text, entities=entities)

    if as_html:
        return message.html_text
    else:
        return message.md_text


menu_keyboard = create_keyboard_reply(["🚌 Поехали"], rows=[1])
