from typing import Annotated
from fastapi import (APIRouter, Depends, HTTPException, status,
                    #   WebSocket, WebSocketDisconnect
                      )
from fastapi.security import OAuth2PasswordRequestForm

from app.config.auth import create_access_token, authenticate_user, get_password_hash, verify_confirmation_token, CurrentUser
from app.schemas.users import Token, UserBase, UserCreate
from app.crud import users, items
from app.db.db import dbDep
from app.utils.mail import send_confirm_email
# from app.config.websocket import connection_manager
# from app.config.grpclient import grpc_client

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: dbDep):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup/")
async def create_user(user: UserCreate, db: dbDep):
    db_user = users.get_user(db, user.username, user.email)
    if db_user and db_user.is_active:
        raise HTTPException(status_code=400, detail="Username is already taken")
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    if db_user:
        db_user = users.update_user(db, db_user.id, user.username, user.email, user.password)
    else:    
        db_user = users.create_user(db, user.username, user.password, user.email)
    await send_confirm_email(db_user.email) 

    return {"username": db_user.username,"message": "Sign up successfully, please check your email for verification"}

    # confirm_link = await send_confirm_email(db_user.email)
    # return {"username": db_user.username,"message": f"Go to {confirm_link} for verification"}

@router.get("/confirm/{token}")
def confirm_signup(token: str, db: dbDep):
    email = verify_confirmation_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    if email=="expired":
        raise HTTPException(status_code=400, detail="Token expired")
    users.confirm_user(db, email)
    return {"message": "Email confirmed"}

@router.get("/users/me", response_model=UserBase)
def get_user_me(current_user: CurrentUser, db: dbDep):
    user = users.get_user(db, current_user)
    return {"username": user.username, "email": user.email}

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: Annotated[WebSocket, Depends()], db: dbDep, current_user: str = Depends(get_current_user)):
#     await connection_manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             me = users.get_user(db, current_user)
#             todo = items.get_items_by_owner(db, me.id)
#             response = await grpc_client.send_message(data)
#             await connection_manager.send_personal_message(f"Bot: {response}", websocket)
#             await connection_manager.broadcast(f"User: {data}")
#     except WebSocketDisconnect:
#         connection_manager.disconnect(websocket)
#         await connection_manager.broadcast(f"User left the chat")

