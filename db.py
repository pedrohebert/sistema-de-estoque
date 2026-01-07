from sqlmodel import Field, SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends



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


SQL_DATABE_FILENAME = "databese.db"
SQL_DATABASE_URL = f"sqlite:///{SQL_DATABE_FILENAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(SQL_DATABASE_URL, connect_args=connect_args)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
