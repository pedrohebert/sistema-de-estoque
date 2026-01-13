from contextlib import asynccontextmanager
from typing import Annotated, Sequence
from fastapi import FastAPI, Query
from starlette.responses import FileResponse
from app.db import  create_db_and_table, SessionDep
from app.models import Item, ItemCreate, ItemPublic, ItemUpdate, OperacaoEStoque, CreateOperacaoEstoque, PublicOperacaoEStoque
from app.services.ItemSevices import CreateItem, DeleteItem, GetItens, GetItensById, UpdateItem
from app.services.OperacaoSevice import CreateOperacao, GetAllOperacao, GetAllOperacaoByItemId, GetByIdOperacao, GetEstoqueItem
from fastapi.middleware.cors import CORSMiddleware

# fim da criação do banco de dados 

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield



app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # em produção, restrinja
    allow_credentials=True,
    allow_methods=["*"],   # permite POST, PATCH, DELETE, OPTIONS
    allow_headers=["*"],   # permite Content-Type
)


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("app/html/index.html")

@app.post("/item/", response_model=ItemPublic)
def create_item(session: SessionDep, item: ItemCreate ) -> Item:
    return CreateItem(session, item)


@app.get("/itens/", response_model=Sequence[ItemPublic])
def get_itens(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[Item]:
    return GetItens(session, offset, limit)

@app.get("/itens/{item_id}", response_model=ItemPublic)
def get_itens_by_id(
    session:SessionDep,
    item_id: int
    ) -> Item:
    return GetItensById(session, item_id)

@app.patch("/item/{item_id}", response_model=ItemPublic)
def update_item(
    session: SessionDep,
    item: ItemUpdate,
    item_id:int) -> Item:
    return UpdateItem(session, item, item_id)

@app.delete("/item/{item_id}")
def delete_item(
    session: SessionDep,
    item_id: int
    ) -> dict[str, bool]:
    return DeleteItem(session, item_id)


@app.post("/op/", response_model=PublicOperacaoEStoque)
def create_operacao(
    session:SessionDep, operacao: CreateOperacaoEstoque
    ) -> OperacaoEStoque:
    return CreateOperacao(session, operacao)

@app.get("/op/", response_model=Sequence[PublicOperacaoEStoque])
def get_all_op(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    return GetAllOperacao(session, offset, limit)

@app.get("/op/{op_id}", response_model=PublicOperacaoEStoque)
def get_by_id_operacao(
    session:SessionDep, op_id:int
    ) -> OperacaoEStoque:
    return GetByIdOperacao(session, op_id)

@app.get("/op/item/{item_id}", response_model=Sequence[PublicOperacaoEStoque])
def get_all_operacao_by_item_id(
    session:SessionDep, item_id:int
    ) -> Sequence[OperacaoEStoque]:
    return GetAllOperacaoByItemId(session, item_id)

@app.get("/item/{item_id}/estoque")
def get_estoque_item(
    session: SessionDep,
    item_id: int
    ) -> int:
    return GetEstoqueItem(session, item_id)

