from pydantic import BaseModel
from datetime import date

class ItemBase(BaseModel):
    title: str
    description: str | None = None
    deadline: date | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True