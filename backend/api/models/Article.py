from pydantic import BaseModel
import uuid


class LegalPublication(BaseModel):
    id: uuid.UUID
    type: str  # e.g. "PCT", "EPC", "EPCGuidelines", "CaseLaw"
    title: str
    url: str
