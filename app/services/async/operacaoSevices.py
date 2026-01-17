from typing import Annotated, Sequence
from fastapi import HTTPException, Query
from sqlmodel import func, select, case
from app.db.db_async import asyncSessionDep
from app.models.models import CreateOperacaoEstoque, Item, OperacaoEStoque, TipoOperacao


async def CreateOperacao(
    session:asyncSessionDep, 
    operacao: CreateOperacaoEstoque 
    ) -> OperacaoEStoque:
    op_db = OperacaoEStoque.model_validate(operacao)

    item_operado = await session.get(Item, op_db.item_id)
    if not item_operado:
        raise HTTPException(status_code=400, detail="item_id invalid")
    
    if op_db.tipo == TipoOperacao.RETIRAR:
        estoque = await GetEstoqueItem(session, op_db.item_id)

        if estoque < op_db.quantidade:
            raise HTTPException(status_code=400, detail="operacao invalid")

    session.add(op_db)
    await session.commit()
    await session.refresh(op_db)
    return op_db


async def GetAllOperacao(
    session: asyncSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    op_db = await session.exec(
        select(OperacaoEStoque)
        .offset(offset)
        .limit(limit)
        )
    return op_db.all()



async def GetAllOperacaoByItemId(
    session:asyncSessionDep,
    item_id:int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    operacoes = await session.exec(
        select(OperacaoEStoque)
        .offset(offset)
        .limit(limit)
        .where(OperacaoEStoque.item_id == item_id)
        )
    return operacoes.all()

async def GetEstoqueItem(
    session: asyncSessionDep,
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

    res = await session.exec(
            select(soma)
            .where(OperacaoEStoque.item_id == item_id)
    )

    return res.one()