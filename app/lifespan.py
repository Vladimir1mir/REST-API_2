from contextlib import asynccontextmanager
from fastapi import FastAPI

from models import init_orm, close_orm


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Выполняются действия при старте приложения
    print("Starting up...")
    await init_orm()

    yield

    # Выполняются действия при остановке приложения
    await close_orm()
    print("Shutting down...")