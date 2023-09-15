from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMGreeting(StatesGroup):
    name = State()
    team = State()


class FSMQuestion(StatesGroup):
    question = State()


class FSMTest(StatesGroup):
    test = State()
