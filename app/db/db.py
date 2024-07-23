from fastapi import Depends
from typing import Annotated, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config.env import env

DATABASE_URL = env.database['url']

engine = create_engine(DATABASE_URL, echo=True)

session_local = sessionmaker(
    bind=engine, autocommit=False, autoflush=False
)

def get_db() -> Generator[Session, None, None]:
    db = session_local()
    try:
        yield db
    finally:
        db.close()

dbDep = Annotated[Session, Depends(get_db)]