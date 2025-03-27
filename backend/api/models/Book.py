from pydantic import BaseModel, Field
import uuid
import datetime
from typing import Optional, List


class Book(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4) # Remove the alias
    title: str 
    categories: list[str]
    type: str
    user_id: uuid.UUID
    created_at: Optional[datetime.datetime] = None

class BookForCreate(BaseModel):
    title: Optional[str] = "book"
    categories: List[str]
    type: str
    user_id: uuid.UUID
