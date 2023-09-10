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

    def __init__(self, body, type, answers=None, cor_answer=None, correct_reply=None, incor_action=Action.stay,
                 picture=None, sticker=None, incorrect_reply=None):
        self.body = body
        self.answers = answers
        self.correct_reply = correct_reply
        self.type = type
        self.picture = picture
        self.sticker = sticker
        self.cor_answer = cor_answer
        self.incor_action = incor_action
        self.incorrect_reply = incorrect_reply
