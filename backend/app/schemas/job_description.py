from pydantic import BaseModel
from datetime import datetime

class JDCreate(BaseModel):
    title: str
    company: str | None = None
    raw_text: str

class JDOut(BaseModel):
    id: str
    title: str
    company: str | None
    created_at: datetime
