import enum
from os import getenv

from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, MetaData, Text, func, Float, Enum, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',

    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',

    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',

    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',

    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}
Base.metadata = MetaData(naming_convention=convention)


class Team(enum.Enum):
    marik = 0
    marea = 1


class User(Base):
    __tablename__ = 'user'

    chat_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String, unique=True, nullable=True)

    name = Column(String(100), nullable=True)
    school = Column(String(200), nullable=True)
    team = Column(Enum(Team))
    register_date = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f'User(name={self.name}, phone_number={self.phone_number}, email={self.email}, role={self.role})'


def get_sessionmaker() -> sessionmaker:
    user = getenv('POSTGRES_USER')
    password = getenv('POSTGRES_PASSWORD')

    engine = create_async_engine(f'postgresql+asyncpg://user:user1234@127.0.0.1:6000/quiz-travel', echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    return async_session
