from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from async_bot.dialog_branches.clients.states import FSMGreeting
from async_bot.dialog_branches.utils import menu_keyboard
from database.crud import update_user
from database.models import User, Team


async def command_start(message: types.Message, session: AsyncSession, user: User, state: FSMContext):
    if user is None:
        user = User(chat_id=message.chat.id, username=message.chat.username, name=message.chat.first_name)
        await update_user(user, session)

        await state.set_state(FSMGreeting.name)
        await message.answer(
            "Привет, я бот #ОткрывайАлтай. Я сделаю твое сегодняшнее путешествие интересней и веселей. А если ты выполнишь все задания - тебя ждет реальный стикер пак с главными Алтайскими маралятами <b>Мариком</b> и <b>Марей</b>.")
        await message.answer("Напиши, как тебя зовут (Имя и фамилия)")
    else:
        await message.answer("#ОткрывайАлтай с <b>Мариком</b> и <b>Марей</b>", reply_markup=menu_keyboard)


async def change_team(message: types.Message, session: AsyncSession, user: User, state: FSMContext):
    if user.team is None:
        await message.answer('Ты пока еще не присоединился ни к одной окманде', reply_markup=ReplyKeyboardRemove())
        return

    if user.team == Team.marik:
        user.team = Team.marea
        await message.answer('Теперь ты в команде "Мари"', reply_markup=menu_keyboard)
    else:
        user.team = Team.marik
        await message.answer('Теперь ты в команде "Марика"', reply_markup=menu_keyboard)

    await update_user(user, session)
    await state.set_state()


async def legend(message: types.Message):
    await message.answer("""Один марал-мальчик родился в синем цвете. В детстве он был очень сильным и ловким маралом. И вот одним ранним весенним утром охотники увидели синего оленя, который очень отличался от здешних лесных обитателей. Они захотели получить его мех. 
Марал услышал выстрел и побежал со всех ног в лесную чащу. Лес был очень густой и маралу приходилось использовать всю свою силу и ловкость, чтобы пробираться сквозь лесную чащу, но охотники не отставали от него и преследовали марала днями и ночами. В один из дней, пробираясь через густо произрастающие сосны, он выбился из сил, ударился о ствол дерева и потерял рог. Охотники взяли этот рог и прекратили поиски синего марала.
Тем временем он выбрался на пригорок, где повсюду цвели кусты маральника. Марал сильно устал и лег на траву отдохнуть. Проснулся он от того, что на него аккуратно издалека смотрела,покрытая розовым мехом, марал-девочка. Она была взволнована, потому что думала, что является единственным цветным маралом. 
Марал взглянул на нее и сразу влюбился! Он медленно и осторожно подошел и подарил ей цветок маральника. С тех самых пор они вместе путешествуют по Алтайскому краю, а девочка-марал никогда не снимает подаренный цветок. 
""")


async def command_creator(message: types.Message):
    await message.answer("Создатель бота: @VlaSerega.")


def register_start_handlers(dp: Dispatcher):
    dp.message.register(command_start, Command("start"))
    dp.message.register(command_creator, Command('creator'))
    dp.message.register(change_team, Command('change_team'))
    dp.message.register(legend, Command('legend'))
