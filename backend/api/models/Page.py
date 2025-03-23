from pydantic import BaseModel
import uuid


class Page(BaseModel):
    id: uuid.UUID
    title: str
    book_id: uuid.UUID
    qa_id: uuid.UUID
    history: list[dict]
    created_at: str


class PageForCreate(BaseModel):
    title: str
    book_id: uuid.UUID
    qa_id: uuid.UUID
