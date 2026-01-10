from contextlib import asynccontextmanager
from typing import Annotated, Sequence
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import func, select, case
from sqlalchemy.exc import IntegrityError
from db import  create_db_and_table, SessionDep
from models import Item, ItemCreate, ItemPublic, ItemUpdate, BaseOperacaoEstoque, OperacaoEStoque, CreateOperacaoEstoque, PublicOperacaoEStoque, TipoOperacao


# fim da criação do banco de dados 

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield



app = FastAPI(lifespan=lifespan)


@app.post("/item/", response_model=ItemPublic)
async def create_item(item: ItemCreate, session: SessionDep) -> Item:
    db_item = Item.model_validate(item)
    try:
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
    except(IntegrityError):
        raise HTTPException(status_code=400, detail="item already exists")
    
    return db_item


@app.get("/itens/", response_model=Sequence[ItemPublic])
def get_itens(
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


@app.post("/op/", response_model=PublicOperacaoEStoque)
def create_operacao(operacao: CreateOperacaoEstoque, session:SessionDep) -> OperacaoEStoque:

    db_op = OperacaoEStoque.model_validate(operacao)

    item_operado = session.get(Item, db_op.item_id)
    if not item_operado:
        raise HTTPException(status_code=400, detail="item_id invalid")
    
    if db_op.tipo == TipoOperacao.RETIRAR:
        estoque =  get_estoque_item(session, db_op.item_id)

        if estoque < db_op.quantidade:
            raise HTTPException(status_code=400, detail="operacao invalid")

    session.add(db_op)
    session.commit()
    session.refresh(db_op)
    return db_op

@app.get("/op/", response_model=Sequence[PublicOperacaoEStoque])
def get_all_op(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    Operacoes = session.exec(select(OperacaoEStoque).offset(offset).limit(limit)).all()
    return Operacoes

@app.get("/op/{op_id}", response_model=PublicOperacaoEStoque)
def get_by_id_operacao(
    op_id:int, session:SessionDep
    ) -> OperacaoEStoque:
    op = session.get(OperacaoEStoque, op_id)
    if not op:
        raise HTTPException(status_code=404, detail="operacao not found")
    return op

@app.get("/op/item/{item_id}", response_model=Sequence[PublicOperacaoEStoque])
def get_all_operacao_by_item_id(
    session:SessionDep, item_id:int
    ) -> Sequence[OperacaoEStoque]:
    operacoes = session.exec(select(OperacaoEStoque).where(OperacaoEStoque.item_id == item_id)).all()
    return operacoes

@app.get("/item/{item_id}/estoque")
def get_estoque_item(
    session: SessionDep,
    item_id: int
    ) -> int:
    soma = func.coalesce( 
        func.sum(
            case(
                (OperacaoEStoque.tipo == TipoOperacao.ADICIONAR, OperacaoEStoque.quantidade),
                (OperacaoEStoque.tipo == TipoOperacao.RETIRAR, -OperacaoEStoque.quantidade),
                else_=0
            )
        ),
        0
    )

    res = session.exec(
            select(soma).where(OperacaoEStoque.item_id == item_id)
    ).one()

    return res 

