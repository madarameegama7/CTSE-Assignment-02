from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class TripResponse(BaseModel):
    destination: str
    days: int
    budget: float
    preferences: List[str]

    itinerary: List[Dict[str, Any]] = Field(default_factory=list)
    cost_breakdown: Dict[str, float] = Field(default_factory=dict)
    total_cost: float = 0.0

    validation_status: str = "PENDING"
    validation_errors: List[str] = Field(default_factory=list)

    recommended_changes: List[str] = Field(default_factory=list)
    output_file: Optional[str] = None

    logs: List[str] = Field(default_factory=list)