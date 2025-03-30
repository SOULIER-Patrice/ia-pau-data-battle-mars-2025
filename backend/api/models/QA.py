from pydantic import BaseModel
import uuid
from typing import Optional, List


class QA(BaseModel):
    id: uuid.UUID
    type: str
    category: str
    question: str
    answer: str
    is_verified: bool
    options: Optional[List[str]] = None
    justification: Optional[str] = None


class QAForCreate(BaseModel):
    categories: List[str]
    type: str
    number: int
