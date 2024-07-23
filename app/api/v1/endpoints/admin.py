from fastapi import APIRouter

from app.crud import items, users
from app import schemas
from app.db.db import dbDep

router =  APIRouter()

@router.get("/items/", response_model=list[schemas.Item])
async def items_list():
    return await items.get_items()

@router.get("/users/", response_model=list[schemas.UserInfo])
async def users_list(db: dbDep):
    return await users.get_users(db)

@router.get("/users/{username}")
async def user_detail(username: str, db: dbDep):
    user = await users.get_user(db, username)
    if user is None:
        return {"message": "User not found"}
    items_list = await items.get_items_by_owner(db, user.id)
    return {**user.__dict__, "items": items_list}
