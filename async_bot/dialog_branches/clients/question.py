import enum


class QuestionType(enum.Enum):
    one = 1
    some = 2
    any = 3
    photo = 4
    sticker = 5


class Action(enum.Enum):
    next = 1
    stay = 2


class Question:

    def __init__(self, body, type=QuestionType.one, answers=None, cor_answer=None, correct_reply=None,
                 incor_action=Action.stay,
                 picture=None, sticker_correct=None, sticker_incor=None, incorrect_reply=None, state=None):
        self.body = body
        self.answers = answers
        self.correct_reply = correct_reply
        self.type = type
        self.picture = picture
        self.sticker_correct = sticker_correct
        self.sticker_incor = sticker_incor
        self.cor_answer = cor_answer
        self.incor_action = incor_action
        self.incorrect_reply = incorrect_reply
        self.state = state
