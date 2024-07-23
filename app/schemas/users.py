from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str 

class UserCreate(UserBase):
    password: str

class UserInfo(UserBase):
    id: int
    role: str
    is_active: bool

class User(UserCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None