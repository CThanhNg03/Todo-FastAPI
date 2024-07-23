from fastapi import APIRouter, Depends

from app.config.auth import CurrentUser
from app.db.db import dbDep
from app.crud import items, users
from app.schemas import items as items_schemas


router =  APIRouter()

@router.get("/myitems/", response_model=list[items_schemas.Item])
def get_my_items(current_user: CurrentUser, db: dbDep):
    me = users.get_user(db, current_user)
    return items.get_items_by_owner(db, me.id)

@router.post("/newitem/", response_model=items_schemas.Item)
def create_item(item: items_schemas.ItemCreate, current_user: CurrentUser, db: dbDep):
    me = users.get_user(db, current_user)
    return items.create_item(db, item.title, item.description, me.id, item.deadline)

@router.get("/done/{item_id}")
def done_item(item_id: int, db: dbDep):
    try:
        item = items.done_item(db, item_id)
        return {"message": f"Item {item.title} is done"}
    except:
        return {"message": "Item not found"}
    
@router.delete("/delete/{item_id}")
def delete_item(item_id: int, db: dbDep):
    try:
        item = items.delete_item(db, item_id)
        return {"message": f"Item {item.title} is deleted"}
    except:
        return {"message": "Item not found"}
