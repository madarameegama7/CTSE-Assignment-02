# Since your individual agents are not ready yet, first add a temporary placeholder workflow.
# This allows frontend/backend testing before all agents are implemented.
# This is temporary. Later you will replace it with LangGraph node execution.

from app.graph.state import TravelState
from app.models.request_models import TripRequest
from app.utils.logger import log_event


def run_travel_workflow(request: TripRequest) -> TravelState:
    logs = []

    logs.append(log_event("System", "Workflow started"))

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

        "logs": logs
    }

    logs.append(log_event("System", "Initial state created"))

    return state