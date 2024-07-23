from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base, User
from app.api import api_router
from app.db.db import engine, session_local
from app.config.auth import get_password_hash
from app.config.filter import FilterMiddleware

def init_db(db: Session):
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        user = User(
            username="admin", 
            email="example@email.com",
            password=get_password_hash("admin"),
            role="admin",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
try:
    db = session_local()
    init_db(db)
finally:
    db.close()

app = FastAPI()
app.add_middleware(FilterMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")