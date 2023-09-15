from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from async_bot.dialog_branches.clients.question import Question
from async_bot.dialog_branches.clients.states import FSMQuestion, FSMTest
from async_bot.dialog_branches.clients.stations import questions
from async_bot.dialog_branches.utils import create_keyboard_reply, process_question
from database.models import User

quest = [
    Question('Ты купец, у тебя небольшое поместье. Дела идут хорошо, но нужно расширяться. Где ты возьмешь деньги?\n\n'
             '<b>1.</b> Возьму в долг у родственников\n<b>2.</b> Буду расширяться на те деньги, что есть\n'
             '<b>3.</b> Обращусь в банк',
             answers=['1', '2', '3'], cor_answer='3'),
    Question('У тебя появились излишки средств, что ты будешь с ними делать?\n\n'
             '<b>1.</b> Куплю еще один дом и обустрою его\n<b>2.</b> Вложу в свое дело\n'
             '<b>3.</b> Отпраздную - соберу друзей и устрою прием...',
             answers=['1', '2', '3'], cor_answer='2'),
    Question('Ты разработал план работы на несколько лет, а он "провалился". Твои действия:\n\n'
             '<b>1.</b> Буду паниковать и уеду в отпуск на пару недель, нужно успокоиться\n'
             '<b>2.</b> С холодной головой проанализирую цифры и действия и придумаю новый план\n'
             '<b>3.</b> Буду и дальше селдовать этому плану, не зря же я столько потратил сил на его написание',
             answers=['1', '2', '3'], cor_answer='2'),
    Question(
        'У вашего друга товарища затрудненная ситуация. Он хочет занять у вас 1000 золотых, обещая вернуть через год. Твои действия:\n\n'
        '<b>1.</b> Принципиально не занимаю, пусть обратиться к кому-то еще\n<b>2.</b> Помогу другу\n'
        '<b>3.</b> Дам под процент',
        answers=['1', '2', '3'], cor_answer='3'),
    Question('У вас запланирована важная встреча, но твой приказчик заболел. Твои действия:\n\n'
             '<b>1.</b> Отправлю на встречу другого работника\n<b>2.</b> Отменю встречу, дождусь, когда приказчик поправится\n'
             '<b>3.</b> Поеду сам',
             answers=['1', '2', '3'], cor_answer='3'),
]


async def start_test(message: types.Message, state: FSMContext, user: User):
    async with state.proxy() as data:
        data['score'] = 0
        data['test_current'] = quest[0]
        data['test_num'] = 0

    await message.answer(quest[0].body,
                         reply_markup=create_keyboard_reply(quest[0].answers, [len(quest[0].answers)]))


async def ask_quest(message: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    test = data['test_current']
    t_num = data['test_num']
    score = data['score']

    if message.text not in test.answers:
        await message.answer('Такого ответа я не вижу!')

    score += message.text == test.cor_answer

    t_num += 1
    if t_num != len(quest):
        await message.answer(quest[t_num].body,
                             reply_markup=create_keyboard_reply(quest[t_num].answers, [len(quest[t_num].answers)]))
        await state.update_data(test_current=quest[t_num], test_num=t_num, score=score)
    else:
        if score >= 4:
            await message.answer(
                'Поздравляю, даже 100 лет назада ты бы смог разбогатеть и стать успешным купцом! Препринимательская жилка, гибкость и твердость характера у тебя в крови. Ты точно знаешь что делать, чтобы капиталы росли и твое дело преуспевало!')
        elif score >= 2:
            await message.answer(
                'Твой успех в купечестве зависит от внешних факторов, возможно тебе стоит больше доверять себе и в моменте быть жестче, ставя интересы своего дела выше личных отношений.')
        else:
            await message.answer(
                'Мне тоже интересно, что бы было, если бы купец 100 лет назад принимал такие решения.  Возможно тебе могло повести, но риски потерять все слишком высоки.')
        await FSMQuestion.question.set()
        q_num = data['current_num']
        question = await process_question(message, questions[user.team][q_num + 1])
        await state.update_data(current=question, current_num=q_num + 1)


def register_test(dp: Dispatcher):
    dp.register_message_handler(start_test, text='Старт', state=FSMTest.test)
    dp.register_message_handler(ask_quest, state=FSMTest.test)
