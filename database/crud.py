from sqlalchemy.future import select

from database.models import User


async def get_user_by_id(chat_id: int, session) -> User:
    query = select(User).filter(User.chat_id == chat_id)

    return (await session.execute(query)).scalars().first()


async def get_all_users(session):
    query = select(User)

    return (await session.execute(query)).scalars()


async def get_user_by_username(username: str, session) -> User:
    query = select(User).filter(User.username == username)

    return (await session.execute(query)).scalars().first()


async def update_user(user: User, session) -> User:
    session.add(user)
    await session.commit()
    return user
