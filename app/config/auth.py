from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import logging

from app.crud.users import get_user
from app.db.db import get_db
from app.config.env import env


SECRET_KEY = env.secret['key']
ALGORITHM = env.secret['algorithm']
ACCESS_TOKEN_EXPIRE_MINUTES = env.secret['access_token_expire_minutes']

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

CurrentUser = Annotated[str, Depends(get_current_user)]

def verify_token(token: str | None):
    if token is None:
        return False
    token = token.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            return False
        return username, role
    except JWTError as e:
        logging.error(e)
        return False
    
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    if user.is_active == False:
        return False
    return user

def create_confirmation_token(email: str):
    expiration = datetime.now() + timedelta(hours=1)
    return jwt.encode({"email": email, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

def verify_confirmation_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            return False
        return email
    except jwt.ExpiredSignatureError:
        return "expired"
    except JWTError:
        return False