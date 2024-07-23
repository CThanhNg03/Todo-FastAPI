from operator import or_
from sqlalchemy.orm import Session

from app.db.base import User

def create_user(db: Session, username: str, password: str, email: str) -> User:
    user = User(username=username, password=password, email=email, is_active=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, username: str, email: str | None = None) -> User:
    return db.query(User).filter(or_(User.username == username, User.email == email)).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return user

def confirm_user(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, username: str, email: str, password: str):
    user = db.query(User).filter(User.id == user_id).first()
    user.username = username
    user.email = email
    user.password = password
    db.commit()
    db.refresh(user)
    return user