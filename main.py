from contextlib import asynccontextmanager
from typing import Annotated, Sequence
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select
from db import Item, ItemCreate, ItemPublic, ItemUpdate, create_db_and_table, SessionDep


# fim da criação do banco de dados 

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield



app = FastAPI(lifespan=lifespan)


@app.post("/item/", response_model=ItemPublic)
async def create_item(item: ItemCreate, session: SessionDep) -> Item:
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.get("/itens/", response_model=Sequence[ItemPublic])
async def get_itens(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[Item]:
    itens = session.exec(select(Item).offset(offset).limit(limit)).all()
    return itens

@app.get("/itens/{item_id}", response_model=ItemPublic)
def get_itens_by_id(
    session:SessionDep,
    item_id: int
    ) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="itens not fould")
    return item

@app.patch("/item/{item_id}", response_model=ItemPublic)
def updateItem(
    session: SessionDep,
    item: ItemUpdate,
    item_id:int
    ):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="item not found")
    item_data = item.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@app.delete("/item/{item_id}")
def deleteItem(
    session: SessionDep,
    item_id: int
    ):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="item not found")
    session.delete(db_item)
    session.commit()
    return {"ok": True}


