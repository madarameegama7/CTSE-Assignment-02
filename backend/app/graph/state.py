from typing import TypedDict, List, Dict, Any, Optional


class TravelState(TypedDict, total=False):
    destination: str
    days: int
    budget: float
    preferences: List[str]

    itinerary: List[Dict[str, Any]]
    planner_output: str

    cost_breakdown: Dict[str, float]
    total_cost: float

    validation_status: str
    validation_errors: List[str]

    recommended_changes: List[str]
    output_file: Optional[str]

    validator_prompt_contract: str
    recommendation_prompt_contract: str

    recommendation_attempts: int
    logs: List[str]