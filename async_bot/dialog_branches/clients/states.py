from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMGreeting(StatesGroup):
    team = State()


class FSMQuestion(StatesGroup):
    question = State()
