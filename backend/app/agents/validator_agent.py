from app.graph.state import TravelState
from app.tools.validate_constraints import validate_constraints
from app.utils.logger import log_event


def validator_agent(state: TravelState) -> TravelState:
    """
    Validate the travel plan stored in shared state.

    The validator checks whether the itinerary satisfies:
    - budget constraint
    - day count constraint
    - itinerary structure
    - per-day activity limits

    Args:
        state: Shared workflow state.

    Returns:
        Updated state with:
        - validation_status
        - validation_errors
        - logs
    """
    state["logs"].append(log_event("Validator Agent", "Validation started"))

    result = validate_constraints(
        itinerary=state.get("itinerary", []),
        total_cost=state.get("total_cost", 0.0),
        budget=state.get("budget", 0.0),
        days=state.get("days", 0)
    )

    state["validation_status"] = result["validation_status"]
    state["validation_errors"] = result["validation_errors"]

    if result["validation_status"] == "VALID":
        state["logs"].append(
            log_event("Validator Agent", "Plan validated successfully")
        )
    else:
        state["logs"].append(
            log_event(
                "Validator Agent",
                f"Plan invalid: {'; '.join(result['validation_errors'])}"
            )
        )

    return state