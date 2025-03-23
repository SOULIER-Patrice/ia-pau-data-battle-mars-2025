from pydantic import BaseModel
import uuid
from typing import Optional


class QAOpen(BaseModel):
    id: uuid.UUID
    category: str
    question: str
    answer: str
    justification: Optional[str]
    isVerified: bool = False


class QAMCQ(BaseModel):
    id: uuid.UUID
    category: str
    question: str
    options: list[str]
    answer: str
    justification: Optional[str]
    isVerified: bool = False
