from sqlmodel import SQLModel, Session, create_engine, false
from typing import Annotated
from fastapi import Depends
import os




#SQL_DATABE_FILENAME = "databese.db"
#SQL_DATABASE_URL = f"sqlite:///{SQL_DATABE_FILENAME}"
SQL_DATABASE_URL = os.getenv("DATABASE_URL")
assert SQL_DATABASE_URL != None, "url do banco de dados não definida"

ECHO_DB:bool = True if os.getenv("ECHO_DB") == 'True' else False

engine = create_engine(SQL_DATABASE_URL, echo=ECHO_DB)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
