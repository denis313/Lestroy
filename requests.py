import logging

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from model import Base, Users


class DatabaseManager:
    def __init__(self, dsn):
        self.engine = create_async_engine(dsn, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.async_session() as session:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

    # add new user
    async def add_user(self, user_data):
        try:
            async with self.async_session() as session:
                new_user = Users(**user_data)
                session.add(new_user)
                await session.commit()
                logging.debug(f'New user added with id: {new_user.user_id}')
                return new_user  # Возвращаем объект нового пользователя
        except IntegrityError as e:
            logging.debug(f'User with data {user_data} already exists')
            return None  # Возвращаем None, если пользователь уже существует
        except SQLAlchemyError as e:
            logging.error(f'Error occurred while adding user: {str(e)}')

    # get all users
    async def get_users(self):
        async with self.async_session() as session:
            result = await session.execute(select(Users))
            all_users = result.scalars()
            users = [user for user in all_users]
            return users

    # delete user
    async def delete_user(self, user_id):
        async with self.async_session() as session:
            stmt = delete(Users).where(Users.user_id == user_id)
            await session.execute(stmt)
            await session.commit()
            logging.debug(f'Delete user by id={user_id}')