from sqlmodel import Field, SQLModel
from datetime import datetime


class ItemBese(SQLModel):
    nome: str = Field(index=True)
    unidade_medida: str = Field(index=True)

class Item(ItemBese, table=True):
    id:int | None = Field(default=None, primary_key=True)

class ItemCreate(ItemBese):
    pass

class ItemPublic(ItemBese):
    id:int

class ItemUpdate(SQLModel):
    nome: str | None = None
    unidade_medida:str | None = None






class BaseOperacaoEstoque(SQLModel):
    item_id : int | None = Field(foreign_key="item.id", description="item operado")
    tipo: str = Field(description="ENTRADA ou SAIDA")
    quantidade: int = Field(gt=0, description="quantidade operada")
    data_hora: datetime = Field(default_factory=datetime.now)

class OperacaoEStoque(BaseOperacaoEstoque, table=True):
    id:int | None = Field(default=None, primary_key=True)

class PublicOperacaoEStoque(BaseOperacaoEstoque):
    id: int

class CreateOperacaoEstoque(BaseOperacaoEstoque):
    pass