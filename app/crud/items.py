from datetime import date
from sqlalchemy.orm import Session

from app.db.base import Item

def create_item(db: Session, title: str, description: str, owner_id: int, deadline: date):
    item = Item(title=title, description=description, owner_id=owner_id, deadline=deadline)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items_by_owner(db: Session, owner_id: int):
    return db.query(Item).filter(Item.owner_id == owner_id).all()

def done_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    item.status = "done"
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(item)
    db.commit()
    return item

def update_item(db: Session, item_id: int, title: str, description: str, deadline: date):
    item = db.query(Item).filter(Item.id == item_id).first()
    item.title = title
    item.description = description
    item.deadline = deadline
    db.commit()
    db.refresh(item)
    return item