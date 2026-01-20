from typing import Annotated, Sequence
from fastapi import HTTPException, Query
from fastapi.responses import HTMLResponse
from app.db.db_async import asyncSessionDep
from app.models.models import Item, ItemCreate, ItemUpdate
from sqlmodel import select


async def GetItens(
    session: asyncSessionDep, 
    offset:int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[Item]:

    itens = await session.exec(select(Item).offset(offset).limit(limit))
    return itens.all()

async def CreateItem(
    session: asyncSessionDep, 
    item: ItemCreate
    ) -> Item:
    db_item = Item.model_validate(item)

    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item

async def GetItemById(
    session: asyncSessionDep,
    item_id: int
    ) -> Item:
    item = await session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="itens not fould")
    return item

async def UpdateItem(
    session: asyncSessionDep,
    update_item: ItemUpdate,
    item_id: int
    ) -> Item:
    item_db = await session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="itens not fould")
    item_data = update_item.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(item_data)
    session.add(item_db)
    await session.commit()
    await session.refresh(item_db)
    return item_db

async def DeleteItem(
    session: asyncSessionDep,
    item_id: int
    ) -> dict[str, bool]:
    item_db = await session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="itens not fould")
    await session.delete(item_db)
    return {"ok": True}

"""
async def itemPage():
    return HTMLResponse("app/html/.html")"""