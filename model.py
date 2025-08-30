from sqlalchemy import BigInteger, Boolean, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id_user: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger, nullable=True, unique=True)

    def __repr__(self) -> str:
        ...
        return f"User: id: {self.id_user}, user_id: {self.user_id}"
