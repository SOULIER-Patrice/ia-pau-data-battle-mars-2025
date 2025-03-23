from pydantic import BaseModel
import uuid


class Book(BaseModel):
    id: uuid.UUID
    title: str
    categories: list[str]
    type: str
    user_id: uuid.UUID
    created_at: str


class BookForCreate(BaseModel):
    title: str
    categories: list[str]
    type: str
    user_id: uuid.UUID
