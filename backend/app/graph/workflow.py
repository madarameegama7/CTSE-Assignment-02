# Since your individual agents are not ready yet, first add a temporary placeholder workflow.
# This allows frontend/backend testing before all agents are implemented.
# This is temporary. Later you will replace it with LangGraph node execution.

from app.graph.state import TravelState
from app.models.request_models import TripRequest
from app.utils.logger import log_event
from app.agents.planner_agent import planner_agent
from app.agents.budget_agent import run_budget_agent
from app.agents.validator_agent import validator_agent
from app.agents.recommendation_agent import recommendation_agent


def run_travel_workflow(request: TripRequest) -> TravelState:
    state: TravelState = {
        "destination": request.destination,
        "days": request.days,
        "budget": request.budget,
        "preferences": request.preferences,
        "itinerary": [],
        "cost_breakdown": {},
        "total_cost": 0.0,
        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": [log_event("System", "Workflow started")]
    }

    state = planner_agent(state)
    state = run_budget_agent(state)
    state = validator_agent(state)

    if state.get("validation_status") == "INVALID":
        state = recommendation_agent(state)
        state = validator_agent(state)

    state["logs"].append(log_event("System", "Workflow completed"))
    return state