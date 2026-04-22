from pydantic import BaseModel, Field
from typing import List


class TripRequest(BaseModel):
    destination: str = Field(..., min_length=1)
    days: int = Field(..., gt=0, le=14)
    budget: float = Field(..., gt=0)
    preferences: List[str] = Field(default_factory=list)