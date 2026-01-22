from enum import Enum
from sqlmodel import Field, SQLModel
from datetime import datetime


class UnidadeMedida(str, Enum):
    unidade = "UNIDADE"
    caixa = "CAIXA"
    litro = "LITRO"

class ItemBese(SQLModel):
    nome: str = Field(index=True, unique=True)
    unidade_medida: UnidadeMedida = Field(index=True)

class Item(ItemBese, table=True):
    id:int | None = Field(default=None, primary_key=True)
    ativo:bool = Field(default=True)

class ItemCreate(ItemBese):
    pass

class ItemPublic(ItemBese):
    id:int

class ItemUpdate(SQLModel):
    nome: str | None = None
    unidade_medida:UnidadeMedida | None = None




class TipoOperacao(str, Enum):
    ADICIONAR = "ADICIONAR"
    RETIRAR = "RETIRAR"

class BaseOperacaoEstoque(SQLModel):
    item_id : int = Field(foreign_key="item.id", description="item operado")
    tipo: TipoOperacao = Field(description="ENTRADA ou RETIRAR")
    quantidade: int = Field(gt=0, description="quantidade operada")
    data_hora: datetime = Field(default_factory=datetime.now)

class OperacaoEStoque(BaseOperacaoEstoque, table=True):
    id:int | None = Field(default=None, primary_key=True)

class PublicOperacaoEStoque(BaseOperacaoEstoque):
    id: int

class CreateOperacaoEstoque(BaseOperacaoEstoque):
    pass