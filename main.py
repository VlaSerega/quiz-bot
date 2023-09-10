import asyncio

from async_bot.telegram_bot import AsyncBot
from database.models import get_sessionmaker


async def main():
    sessionmaker = get_sessionmaker()
    bot = AsyncBot(sessionmaker)

    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())