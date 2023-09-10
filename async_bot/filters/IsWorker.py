from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


class IsWorker(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        data = ctx_data.get()
        print(data)
        user = data["user"]

        return user.role == "Worker"
