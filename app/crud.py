from fastapi import HTTPException
from models import MODEL, MODEL_TYPE
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

async def add_item(session: AsyncSession, item: MODEL):
    session.add(item)
    try:
        await session.commit()

    except IntegrityError as err:
        raise HTTPException(409, detail="item already exist")


async def get_item_by_id(
    session: AsyncSession, model_type: MODEL_TYPE, item_id: int) -> MODEL:
    item = await session.get(model_type, item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"{model_type.__name__} not found",
        )
    return item


async def delete_item(session: AsyncSession, item: MODEL):
    await session.delete(item)
    await session.commit()


