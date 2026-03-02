from pydantic import BaseModel
from typing import Literal

class MatchCreate(BaseModel):
    resume_id: str
    jd_id: str
    preset: Literal["swe", "ml", "data"]  = "swe"
