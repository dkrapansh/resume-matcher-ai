from pydantic import BaseModel
from datetime import datetime

class ResumeOut(BaseModel):
    id: str
    filename: str
    created_at: datetime

    class Config:
        from_attributes = True
