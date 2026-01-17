from typing import Annotated, Sequence
from fastapi import APIRouter, Query
from app.models.models import Item, ItemCreate, ItemPublic, ItemUpdate, OperacaoEStoque, CreateOperacaoEstoque, PublicOperacaoEStoque
from app.services.asyncio.itemServices import CreateItem, DeleteItem, GetItens, GetItemById, UpdateItem
from app.services.asyncio.operacaoSevices import CreateOperacao, GetAllOperacao, GetAllOperacaoByItemId, GetEstoqueItem, GetByIdOperacao
from app.db.db_async import asyncSessionDep

asyncRoute = APIRouter()


@asyncRoute.post("/item/", response_model=ItemPublic)
async def create_item(session: asyncSessionDep, item: ItemCreate ) -> Item:
    return await CreateItem(session, item)


@asyncRoute.get("/itens/", response_model=Sequence[ItemPublic])
async def get_itens(
    session: asyncSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[Item]:
    return await GetItens(session, offset, limit)

@asyncRoute.get("/itens/{item_id}", response_model=ItemPublic)
async def get_itens_by_id(
    session:asyncSessionDep,
    item_id: int
    ) -> Item:
    return await GetItemById(session, item_id)

@asyncRoute.patch("/item/{item_id}", response_model=ItemPublic)
async def update_item(
    session: asyncSessionDep,
    item: ItemUpdate,
    item_id:int) -> Item:
    return await UpdateItem(session, item, item_id)

@asyncRoute.delete("/item/{item_id}")
async def delete_item(
    session: asyncSessionDep,
    item_id: int
    ) -> dict[str, bool]:
    return await DeleteItem(session, item_id)


@asyncRoute.post("/op/", response_model=PublicOperacaoEStoque)
async def create_operacao(
    session:asyncSessionDep, operacao: CreateOperacaoEstoque
    ) -> OperacaoEStoque:
    return await CreateOperacao(session, operacao)

@asyncRoute.get("/op/", response_model=Sequence[PublicOperacaoEStoque])
async def get_all_op(
    session: asyncSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    return await GetAllOperacao(session, offset, limit)

@asyncRoute.get("/op/{op_id}", response_model=PublicOperacaoEStoque)
async def get_by_id_operacao(
    session:asyncSessionDep, op_id:int
    ) -> OperacaoEStoque:
    return await GetByIdOperacao(session, op_id)

@asyncRoute.get("/op/item/{item_id}", response_model=Sequence[PublicOperacaoEStoque])
async def get_all_operacao_by_item_id(
    session:asyncSessionDep, item_id:int
    ) -> Sequence[OperacaoEStoque]:
    return await GetAllOperacaoByItemId(session, item_id)

@asyncRoute.get("/item/{item_id}/estoque")
async def get_estoque_item(
    session: asyncSessionDep,
    item_id: int
    ) -> int:
    return await GetEstoqueItem(session, item_id)

