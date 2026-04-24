from typing import TypedDict, List, Dict, Any, Optional


class TravelState(TypedDict):
    destination: str
    days: int
    budget: float
    preferences: List[str]

    itinerary: List[Dict[str, Any]]
    cost_breakdown: Dict[str, float]
    total_cost: float

    validation_status: str
    validation_errors: List[str]

    recommended_changes: List[str]
    output_file: Optional[str]

    logs: List[str]