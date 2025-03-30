from pydantic import BaseModel, Field
import uuid
from typing import Optional, List
import datetime


class Page(BaseModel):
    id: uuid.UUID
    title: str
    book_id: uuid.UUID
    history: list[dict]
    created_at: datetime.datetime
    qa_id: uuid.UUID


class PageOuput(BaseModel):
    id: uuid.UUID
    title: str
    book_id: uuid.UUID
    history: list[dict]
    created_at: datetime.datetime

    qa_id: uuid.UUID
    categories: list[str]
    question: str
    options: Optional[List[str]]
    answer: str
    justification: Optional[str]
    isVerified: bool = False


class PageForCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)  # Remove the alias
    title: str  # category + question
    book_id: uuid.UUID
    qa_id: uuid.UUID
