from typing import Annotated, Sequence
from fastapi import HTTPException, Query
from sqlmodel import func, select, case
from app.db import SessionDep
from app.models import CreateOperacaoEstoque, Item, OperacaoEStoque, TipoOperacao


def CreateOperacao(session:SessionDep, operacao: CreateOperacaoEstoque ) -> OperacaoEStoque:

    db_op = OperacaoEStoque.model_validate(operacao)

    item_operado = session.get(Item, db_op.item_id)
    if not item_operado:
        raise HTTPException(status_code=400, detail="item_id invalid")
    
    if db_op.tipo == TipoOperacao.RETIRAR:
        estoque =  GetEstoqueItem(session, db_op.item_id)

        if estoque < db_op.quantidade:
            raise HTTPException(status_code=400, detail="operacao invalid")

    session.add(db_op)
    session.commit()
    session.refresh(db_op)
    return db_op

def GetAllOperacao(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    Operacoes = session.exec(select(OperacaoEStoque).offset(offset).limit(limit)).all()
    return Operacoes


def GetByIdOperacao(
    session:SessionDep, op_id:int
    ) -> OperacaoEStoque:
    op = session.get(OperacaoEStoque, op_id)
    if not op:
        raise HTTPException(status_code=404, detail="operacao not found")
    return op

def GetAllOperacaoByItemId(
    session:SessionDep,
    item_id:int,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ) -> Sequence[OperacaoEStoque]:
    operacoes = session.exec(
        select(OperacaoEStoque)
        .offset(offset)
        .limit(limit)
        .where(OperacaoEStoque.item_id == item_id)
        ).all()
    return operacoes


def GetEstoqueItem(
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