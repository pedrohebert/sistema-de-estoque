from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends
import os




#SQL_DATABE_FILENAME = "databese.db"
#SQL_DATABASE_URL = f"sqlite:///{SQL_DATABE_FILENAME}"
SQL_DATABASE_URL = os.getenv("DATABASE_URL")
assert SQL_DATABASE_URL != None, "url do banco de dados não definida"

print(SQL_DATABASE_URL)

connect_args = {"check_same_thread": False}
engine = create_engine(SQL_DATABASE_URL, connect_args=connect_args, echo=True)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
