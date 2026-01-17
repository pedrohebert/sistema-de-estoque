from typing import Annotated, Sequence
from fastapi import HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from app.db.db import SessionDep
from app.models.models import Item, ItemCreate, ItemUpdate


def CreateItem(session: SessionDep, item: ItemCreate) -> Item:
    db_item = Item.model_validate(item)
    try:
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
    except(IntegrityError):
        raise HTTPException(status_code=400, detail="item already exists")
    
    return db_item

def GetItens(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100) -> Sequence[Item]:

    itens = session.exec(
        select(Item)
        .offset(offset)
        .limit(limit)
    ).all()
    return itens

def GetItemById(
    session:SessionDep,
    item_id: int
    ) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="itens not fould")
    return item

def UpdateItem(
    session: SessionDep,
    item: ItemUpdate,
    item_id:int) -> Item:
    
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="item not found")
    item_data = item.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def DeleteItem(
    session: SessionDep,
    item_id: int
    ) -> dict[str, bool]:
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="item not found")
    session.delete(db_item)
    session.commit()
    return {"ok": True}