from copy import deepcopy
from typing import Any

from app.graph.state import TravelState
from app.tools.cost_calculator import calculate_trip_cost
from app.utils.logger import log_event


AGENT_NAME = "BudgetAgent"


def run_budget_agent(state: TravelState) -> TravelState:
    """Estimate trip costs and add budget information to the global state.

    The budget agent is intentionally tool-first: it delegates numeric
    calculation to ``calculate_trip_cost`` so the LLM cannot hallucinate totals.
    """
    updated_state: TravelState = deepcopy(state)
    logs = list(updated_state.get("logs", []))

    logs.append(log_event(AGENT_NAME, "Starting trip cost calculation"))

    try:
        result = calculate_trip_cost(
            destination=str(updated_state["destination"]),
            days=int(updated_state["days"]),
            itinerary=_safe_itinerary(updated_state.get("itinerary", [])),
        )
    except (KeyError, TypeError, ValueError) as exc:
        logs.append(log_event(AGENT_NAME, f"Cost calculation failed: {exc}"))
        updated_state["cost_breakdown"] = {}
        updated_state["total_cost"] = 0.0
        updated_state["validation_status"] = "INVALID"
        updated_state["validation_errors"] = [
            *updated_state.get("validation_errors", []),
            f"Budget calculation error: {exc}",
        ]
        updated_state["logs"] = logs
        return updated_state

    updated_state["cost_breakdown"] = result["cost_breakdown"]
    updated_state["total_cost"] = result["total_cost"]
    updated_state["logs"] = logs + [
        log_event(AGENT_NAME, f"Total trip cost calculated: {result['total_cost']}")
    ]

    return updated_state


def _safe_itinerary(value: Any) -> list[dict[str, Any]]:
    """Validate the state value enough before sending it to the cost tool."""
    if not isinstance(value, list):
        raise ValueError("State itinerary must be a list.")
    return value
