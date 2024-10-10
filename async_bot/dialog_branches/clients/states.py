from aiogram.fsm.state import State, StatesGroup


class FSMGreeting(StatesGroup):
    name = State()
    team = State()


class FSMQuestion(StatesGroup):
    question = State()


class FSMTest(StatesGroup):
    test = State()
