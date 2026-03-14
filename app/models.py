import datetime
import uuid

from sqlalchemy import ForeignKey, DateTime, String, Integer, Float, UUID, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from special_types import ROLE

from config import PG_DSN

print(PG_DSN)
engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    @property
    def id_dict(self):
        return {"id": self.id}

# Таблица токенов пользователей
class Token(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, unique=True, server_default=func.gen_random_uuid()
    )
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates="tokens")

    @property
    def dict(self):
        return {"token": self.token}

# Таблица пользователей
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[ROLE] = mapped_column(String, default="user")
    tokens: Mapped[list["Token"]] = relationship(
        "Token", lazy="joined", cascade= "all, delete",
        back_populates="user"
    )
    adverts: Mapped[list["Adv"]] = relationship(
        "Adv", lazy="joined", cascade= "all, delete",
        back_populates="user"
    )

    @property
    def dict(self):
        return {"id": self.id, "name": self.name, "role": self.role}



class Adv(Base):
    __tablename__ = "adv"

    id: Mapped[int] = mapped_column(Integer,
        primary_key=True)
    title: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    price: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    author: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )
    user: Mapped["User"] = relationship(
        "User", lazy="joined", back_populates="adverts"
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author": self.author,
            "creation_time": self.creation_time.isoformat(),
        }

MODEL = Adv | User | Token
MODEL_TYPE = type[Adv] | type[User] | type[Token]


async def init_orm():
    async with engine.begin() as coon:
        # Строка для очистки существующей БД,
        # в случае необходимости - раскомментировать
        # await coon.run_sync(Base.metadata.drop_all)
        await coon.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()