from typing import Annotated, Sequence
from fastapi import APIRouter, Query
from app.models.models import Item, ItemCreate, ItemPublic, ItemUpdate, OperacaoEStoque, CreateOperacaoEstoque, PublicOperacaoEStoque
from app.services.ItemServices import CreateItem, DeleteItem, GetItens, GetItemById, UpdateItem
from app.services.OperacaoService import CreateOperacao, GetAllOperacao, GetAllOperacaoByItemId, GetEstoqueItem, GetByIdOperacao
from app.db.db import SessionDep

routes = APIRouter()

@routes.post("/item/", response_model=ItemPublic)
def create_item(session: SessionDep, item: ItemCreate ) -> Item:
    return CreateItem(session, item)


@routes.get("/itens/", response_model=Sequence[ItemPublic])
def get_itens(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[Item]:
    return GetItens(session, offset, limit)

@routes.get("/itens/{item_id}", response_model=ItemPublic)
def get_itens_by_id(
    session:SessionDep,
    item_id: int
    ) -> Item:
    return GetItemById(session, item_id)

@routes.patch("/item/{item_id}", response_model=ItemPublic)
def update_item(
    session: SessionDep,
    item: ItemUpdate,
    item_id:int) -> Item:
    return UpdateItem(session, item, item_id)

@routes.delete("/item/{item_id}")
def delete_item(
    session: SessionDep,
    item_id: int
    ) -> dict[str, bool]:
    return DeleteItem(session, item_id)


@routes.post("/op/", response_model=PublicOperacaoEStoque)
def create_operacao(
    session:SessionDep, operacao: CreateOperacaoEstoque
    ) -> OperacaoEStoque:
    return CreateOperacao(session, operacao)

@routes.get("/op/", response_model=Sequence[PublicOperacaoEStoque])
def get_all_op(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    return GetAllOperacao(session, offset, limit)

@routes.get("/op/{op_id}", response_model=PublicOperacaoEStoque)
def get_by_id_operacao(
    session:SessionDep, op_id:int
    ) -> OperacaoEStoque:
    return GetByIdOperacao(session, op_id)

@routes.get("/op/item/{item_id}", response_model=Sequence[PublicOperacaoEStoque])
def get_all_operacao_by_item_id(
    session:SessionDep, item_id:int
    ) -> Sequence[OperacaoEStoque]:
    return GetAllOperacaoByItemId(session, item_id)

@routes.get("/item/{item_id}/estoque")
def get_estoque_item(
    session: SessionDep,
    item_id: int
    ) -> int:
    return GetEstoqueItem(session, item_id)

@routes.get("/ping")
def pong():
    return {"pong":True}