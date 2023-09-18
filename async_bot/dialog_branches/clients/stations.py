import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from async_bot.dialog_branches.clients.question import QuestionType, Question, Action
from async_bot.dialog_branches.clients.states import FSMQuestion, FSMTest
from async_bot.dialog_branches.utils import process_question, callback_data_answer, Button, \
    create_keyboard_inline, process_remain_question, create_keyboard_reply
from database.models import User, Team

aq = [Question('Ты уже в музее Германа Титова в селе Полковниково?',
               QuestionType.one, answers=['Да', 'Нет'],
               cor_answer='Да',
               incorrect_reply='Скоро прибудешь туда. Не забудь протереть камеру телефона, она понадобиться, чтобы выполнить следующее задание.\n'
                               'Нажми <b>“Да”</b>, как доберешься до пункта назначения!'),
      Question(
          'Отлично! Герман Титов - второй летчик-космонавт в мире и первый человек, совершивший длительный космический полет. А как на счёт selfie c Германом Степановичем? Cделай фото с любым портретом Титова в музее и пришли мне. Собираю коллекцию. 📸',
          QuestionType.photo),
      Question('Класс! Вы отлично смотритесь вместе! Тебе нравится фото?',
               QuestionType.one, answers=['Да', 'Нет'], incor_action=Action.next, cor_answer='Да',
               incorrect_reply='Ну и ладно! Нашe путешествие все-равно продолжается!'),
      Question('Ого! Да вы кажется похожи, случайно не родственники?',
               QuestionType.one, answers=['Да', 'Нет'], incor_action=Action.next, cor_answer='Да',
               incorrect_reply='Ну и ладно! Нашe путешествие все-равно продолжается!'),
      Question('Ещё один ценный кадр для моей коллекции! Пригласить тебя на выставку?',
               QuestionType.one, answers=['Да', 'Нет'], incor_action=Action.next, cor_answer='Да',
               incorrect_reply='Ну и ладно! Нашe путешествие все-равно продолжается!'),
      Question('Классное фото получилось! Тебе понравилось в музее?',
               QuestionType.one, answers=['Да', 'Нет'], incor_action=Action.next, cor_answer='Да',
               incorrect_reply='Ну и ладно! Нашe путешествие все-равно продолжается!'),
      Question('А это точно Герман Степанович? Что-то не похож.',
               QuestionType.one, answers=['Да', 'Нет'], incor_action=Action.next, cor_answer='Да',
               incorrect_reply='Ну и ладно! Нашe путешествие все-равно продолжается!'),
      Question(
          'Продолжаем #ОткрыватьАлтай! А ты знаешь как исторически называется дорога по которой мы едем? Она соединяет Новосибирск и Монголию.',
          QuestionType.one, answers=['Алтайская трасса', 'Чуйский тракт', 'Сибирский тракт'],
          cor_answer='Чуйский тракт',
          incorrect_reply='Классное название, но не верно. Попробуй ещё раз!'),

      Question(
          'Верно! Это Чуйский тракт! Самая красивая дорога Сибири, ТОП -10 дорог мира по версии National Geographic, транспортная артерия, по которой издревле ходили караваны с товарами из Сибири в Монголию, Китай, Казахстан! Чтобы выполнить следующее задание, нужно внимательно слушать экскурсовода. Готов погрузиться в историю Чуйского тракта?',
          QuestionType.one, answers=['Да', 'Нет'], incor_action=Action.next, cor_answer='Да',
          correct_reply='Отлично, тогда слушай внимательно и когда будешь готов, ответь:',
          incorrect_reply='Ну что ж. Я тоже не всегда слушаю экскурсовода. Придется тебе угадывать или воспользоваться помощью друга.'),
      Question(
          'Какая длина у Чуйского тракта?',
          QuestionType.one, answers=['953 км', '1888 км', '370 км'],
          cor_answer='953 км',
          correct_reply='Верно! Длина Чуйского тракта от Новосибирска до границы с Монголией 953 км.',
          incorrect_reply='Кажется ты немного ошибся, попробуй ещё раз.'),
      Question(
          'Вы уже добрались до Бийска?',
          QuestionType.one, answers=['Да', 'Еще нет'],
          cor_answer='Да', sticker_correct='CAACAgIAAxkBAAPiZPw8yOqJhylJAwoJ5Xket9hNGGYAArQsAAKucNBIdMQwb5fhvYQwBA',
          incorrect_reply='Да, расстояние до Бийска немаленькое -  162 км от Барнаула.  Если тебе скучно, спроси у экскурсовода: Где живет бобер?\n'
                          'Нажми <b>“Да”</b>, как доберешься до пункта назначения!'),

      Question(
          'Отлично! Бийск - один из моих любимых городов Алтайского края! Он был образован по указу Петра I, здесь много старых зданий, мистических легенд и загадок, а значит - много приключений! Нажми кнопку "Я в Бийске!" сразу, как въедешь в город.',
          QuestionType.one, answers=['Я в Бийске'], incor_action=Action.next,
          cor_answer='Я в Бийске', ),
      Question(
          'Отлично! Видел какие усы у Великого императора? Сделай себе такие же с помощью пальцев и сфотографируйсся вместе с друзьями возле памятника Петру I. Жду фото в чате, это должно быть очень забавно.',
          QuestionType.photo, sticker_correct='CAACAgIAAxkBAAIDBmUCo1rrURMszOzZTEwRbBlZSIv-AAJ6NQACTyjRSM7mUyhJ7UrzMAQ',
          correct_reply='Ахаха, очень крутое фото получилось!'),
      Question(
          'А теперь мы посетим один из музеев Бийска - старый особняк. С привидениями 👻. Если выберешься оттуда, дай знать, как тебе такая ЭКСКУРСИЯ 😱.\n(Жду от тебя стикер)',
          QuestionType.sticker,
          sticker_correct='CAACAgIAAxkBAAIBnWT8UNABp6abpY-8nOxv0nXTllZPAAJJLQACwCjZSJklXdyBsY7eMAQ',
          correct_reply='Я так и думал! Мне тоже там бывает не по себе.'),
      Question('А ты знал, что Бийск - купеческий город?', QuestionType.one, answers=['Да', 'Нет'],
               incor_action=Action.next, cor_answer='Да', correct_reply='Здорово, что ты слушаешь экскурсовода!',
               incorrect_reply='Я тоже не всегда слушаю экскурсовода.'),
      Question(
          'Я придумал тест, который подскажет, смог ли ты стать успешным купцом (бизнесменом) 100 лет назад, жми "Cтарт" и поехали!',
          QuestionType.one, answers=['Старт'], cor_answer='Старт', state=FSMTest.test),
      Question(
          'Сейчас мы посетим Бийское архиерейское подворье. Здание подворья построено в 1880 году.  Да, да, тогда ещё не родилась даже твоя бабушка. Будь внимателен на экскурсии и запоминай, комнаты каких цветов есть в подворье. После того, как посетишь экскурсию, выбери стикер, с твоей эмоцией от этого места.',
          QuestionType.sticker),
      Question(
          'Класс! Вижу, что Архиерейское подворье не оставило тебя равнодушным. Комната какого цвета понравилась тебе больше всего?',
          QuestionType.any, answers=['🔴 Красный', '🟡 Желтый', '🟢 Зеленый', '🔵 Синий']),
      Question('Самое время продолжить наше путешествие', QuestionType.one, answers=['Продолжить путешествие'],
               cor_answer='Продолжить путешествие'),
      Question(
          'Ну что, нас ждет обратная дорога, возвращаемся в столицу Алтайского края - город Барнаул! Отправь стикер с которым у тебя ассоциируется этот город.',
          QuestionType.sticker,
          sticker_correct='CAACAgIAAxkBAAIDCmUCpJ9MdEymhmBKseNVheHK7qEDAAJ9LQACLpDYSExlbu0ojEi7MAQ'),
      Question(
          'Поздравляем! Ты успешно прошел квест #ОткрывайАлтай! Покажи экскурсоводу это сообщение и получи свой приз!',
          QuestionType.one, answers=['Забрал подарок'],
          sticker_correct='CAACAgIAAxkBAAIDCmUCpJ9MdEymhmBKseNVheHK7qEDAAJ9LQACLpDYSExlbu0ojEi7MAQ',
          cor_answer='Забрал подарок'
      ),
      Question(
          'Класс! Но это ещё не все! Теперь ты можешь всегда пользоваться стикерами с Марей и Мариком, для этого сохрани их себе, если не сделал этого раньше\n\n'
          'А ещё мы с Марей создали чат, где ты можешь общаться и делиться впечатлниями с такими же Открывателями Алтая! Переходи по ссылке, чтобы продолжить приключения с нами! (ссылка на чат/канал)',
          QuestionType.one, answers=['Завершить'], cor_answer='Завершить'
      ),
      Question('На сегодня это все! Мы продолжим наше путешествие завтра.\nНажми завтра кнопку "Едем дальше!"',
               answers=['Едем дальше!'], cor_answer='Едем дальше!')
      ]

questions = {
    Team.marik: [aq[0], aq[1], aq[2:7], aq[7], aq[8], aq[9], aq[10], aq[11], aq[12], aq[13], aq[14], aq[15], aq[22],
                 aq[16], aq[17], aq[18], aq[19], aq[20], aq[21]],
    Team.marea: [aq[9], aq[10], aq[11], aq[12], aq[16], aq[17], aq[14], aq[15], aq[22], aq[0],
                 aq[1], aq[2:7], aq[18], aq[19], aq[20], aq[21]]
}


async def go(message: types.Message, user: User):
    await FSMQuestion.question.set()
    state = Dispatcher.get_current().current_state()

    async with state.proxy() as data:
        data['current'] = questions[user.team][0]
        data['current_num'] = 0
        data['selected_answers'] = []
        data['start'] = datetime.datetime.now()

    await process_question(message, questions[user.team][0])


def select_symbol(a_id, s_answer):
    if a_id in s_answer:
        return "🟢"
    else:
        return "⚪"


async def callback_answer(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    answer_id = int(callback_data['answer_id'])

    async with state.proxy() as data:
        question = data['current']
        if answer_id in data['selected_answers']:
            data['selected_answers'].remove(answer_id)
        else:
            data['selected_answers'].append(answer_id)
        s_answer = data['selected_answers']

    answers = question.answers
    buttons = [Button(f"{select_symbol(a.id, s_answer)} {a.answer}",
                      callback_data_answer.new(answer_id=a.id)) for a in answers]
    rows = [2 if (i + 1) * 2 <= len(buttons) else 1 for i in range((len(buttons) + 1) // 2)]
    buttons.append(Button('Ответить', 'Ответ'))
    rows.append(1)

    keyboard = create_keyboard_inline(buttons, rows)
    await callback.message.edit_reply_markup(reply_markup=keyboard)


async def callback_send_answers(callback: types.CallbackQuery, session: AsyncSession, user: User, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    data = await state.get_data()
    question = data['current']
    start = data['start']
    remain = data['remain_questions']
    s_answer = data['selected_answers']

    answers = question.answers
    delta = datetime.datetime.now() - start
    elapsed_time = delta.seconds + (delta.microseconds // 10000) / 100
    score = max(sum([a.score if a.id in s_answer else 0 for a in answers]), 0)

    # await create_or_update_user_answer(session, user.chat_id, question.id, elapsed_time, score)
    await process_remain_question(callback.message, remain, state, session)


async def message_answer(message: types.Message, user: User, state: FSMContext):
    data = await state.get_data()
    question = data['current']
    q_num = data['current_num']
    next = q_num

    if question.type != QuestionType.one:
        await message.delete()
        return

    text = message.text
    if text != question.cor_answer:
        if question.incorrect_reply is None:
            await message.delete()
            return
        if question.incor_action == Action.next:
            keyboard = None
            next = q_num + 1
        else:
            keyboard = create_keyboard_reply(question.answers, [len(question.answers)])
        if question.sticker_incor is not None:
            await message.answer_sticker(question.sticker_incor)
        await message.answer(question.incorrect_reply, reply_markup=keyboard)
    else:
        if question.correct_reply is not None:
            await message.answer(question.correct_reply)
        if question.sticker_correct is not None:
            await message.answer_sticker(question.sticker_correct)
        next = q_num + 1

    if next >= len(questions[user.team]):
        await state.finish()
        await message.answer("Путешествие закончилось!", reply_markup=ReplyKeyboardRemove())
        return
    if q_num != next:
        question = await process_question(message, questions[user.team][q_num + 1])
        await state.update_data(current=question, current_num=q_num + 1)


async def photo_answer(message: types.Message, user: User, state: FSMContext):
    data = await state.get_data()
    question = data['current']
    q_num = data['current_num']
    if question.type != QuestionType.photo:
        await message.delete()
        return

    if q_num + 1 >= len(questions[user.team]):
        await state.finish()
        await message.answer("Путешествие закончилось!", reply_markup=ReplyKeyboardRemove())
        return

    question = await process_question(message, questions[user.team][q_num + 1])
    await state.update_data(current=question, current_num=q_num + 1)


async def sticker_answer(message: types.Message, user: User, state: FSMContext):
    data = await state.get_data()
    question = data['current']
    q_num = data['current_num']
    if question.type != QuestionType.sticker:
        await message.delete()
        return

    if q_num + 1 >= len(questions[user.team]):
        await state.finish()
        await message.answer("Путешествие закончилось!", reply_markup=ReplyKeyboardRemove())
        return

    question = await process_question(message, questions[user.team][q_num + 1])
    await state.update_data(current=question, current_num=q_num + 1)


async def red_room(message: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    question = data['current']
    q_num = data['current_num']
    if question.type != QuestionType.any:
        await message.delete()
        return

    await message.answer(
        'Красный - самый яркий, огненный цвет. В этой комнате раньше был кабинет важной личности. Твой выбор означает, что ты сильная личность, у тебя много энергии, ты умеешь руководить, не боишься брать на себя ответственность и принимать сложные решения.')

    if q_num + 1 >= len(questions[user.team]):
        await state.finish()
        await message.answer("Путешествие закончилось!", reply_markup=ReplyKeyboardRemove())
        return

    question = await process_question(message, questions[user.team][q_num + 1])
    await state.update_data(current=question, current_num=q_num + 1)


async def yellow_room(message: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    question = data['current']
    q_num = data['current_num']
    if question.type != QuestionType.any:
        await message.delete()
        return

    await message.answer(
        'В этой комнате часто проходили важные собрания, в которых всегда присутсововал лидер. Желтый - цвет лидера, если ты выбрал эту комнату, значит в тебе есть лидерские качества, способность объединять и вести за собой.')
    if q_num + 1 >= len(questions[user.team]):
        await state.finish()
        await message.answer("Путешествие закончилось!", reply_markup=ReplyKeyboardRemove())
        return

    question = await process_question(message, questions[user.team][q_num + 1])
    await state.update_data(current=question, current_num=q_num + 1)


async def green_room(message: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    question = data['current']
    q_num = data['current_num']
    if question.type != QuestionType.any:
        await message.delete()
        return

    await message.answer(
        'В этой комнате раньше был кабинет, где день за днем кипела размеренная работа. Выбор этой комнаты говорит о том, что ты спокойный, уравновешенный, интеллектально разивит, терпелив, можешь выполнять сложные  и объёмные задачи.')
    if q_num + 1 >= len(questions[user.team]):
        await state.finish()
        await message.answer("Путешествие закончилось!", reply_markup=ReplyKeyboardRemove())
        return

    question = await process_question(message, questions[user.team][q_num + 1])
    await state.update_data(current=question, current_num=q_num + 1)


async def blue_room(message: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    question = data['current']
    q_num = data['current_num']
    if question.type != QuestionType.any:
        await message.delete()
        return

    await message.answer(
        'В этой комнате ранее проводились разного рода собрания и принимались важные решения., если ты выбрал эту комнату, это говорит о том, что ты очень общительный и у тебя много друзей, ты умеешь поддерживать непринуждную и легкую атмосферу в коллективе.')
    if q_num + 1 >= len(questions[user.team]):
        await state.finish()
        await message.answer("Путешествие закончилось!", reply_markup=ReplyKeyboardRemove())
        return

    question = await process_question(message, questions[user.team][q_num + 1])
    await state.update_data(current=question, current_num=q_num + 1)


def register_stations(dp: Dispatcher):
    dp.register_message_handler(go, text="🚌 Поехали", chat_type=types.ChatType.PRIVATE)
    # dp.register_callback_query_handler(callback_answer, callback_data_answer.filter(), state=FSMQuestion.question)
    # dp.register_callback_query_handler(callback_send_answers, CallbackData('Ответ').filter(),
    #                                    state=FSMQuestion.question)
    dp.register_message_handler(red_room, text='🔴 Красный', state=FSMQuestion.question)
    dp.register_message_handler(yellow_room, text='🟡 Желтый', state=FSMQuestion.question)
    dp.register_message_handler(green_room, text='🟢 Зеленый', state=FSMQuestion.question)
    dp.register_message_handler(blue_room, text='🔵 Синий', state=FSMQuestion.question)
    dp.register_message_handler(message_answer, state=FSMQuestion.question)
    dp.register_message_handler(photo_answer, content_types=types.ContentType.PHOTO, state=FSMQuestion.question)
    dp.register_message_handler(sticker_answer, content_types=types.ContentType.STICKER, state=FSMQuestion.question)
