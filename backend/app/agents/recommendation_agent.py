from copy import deepcopy
from typing import Any, Dict, List

from app.graph.state import TravelState
from app.tools.file_writer import write_itinerary_to_file
from app.utils.logger import log_event


def _reduce_activities(itinerary: List[Dict[str, Any]], max_activities_per_day: int = 2) -> List[Dict[str, Any]]:
    """
    Reduce activities per day to a maximum threshold.
    """
    updated_itinerary = deepcopy(itinerary)

    for day_plan in updated_itinerary:
        activities = day_plan.get("activities", [])
        if isinstance(activities, list) and len(activities) > max_activities_per_day:
            day_plan["activities"] = activities[:max_activities_per_day]

    return updated_itinerary


def _fill_empty_days(itinerary: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Fill empty day activities with a placeholder recommendation.
    """
    updated_itinerary = deepcopy(itinerary)

    for day_plan in updated_itinerary:
        activities = day_plan.get("activities", [])
        if isinstance(activities, list) and len(activities) == 0:
            day_plan["activities"] = ["Free exploration"]

    return updated_itinerary


def _match_day_count(itinerary: List[Dict[str, Any]], days: int) -> List[Dict[str, Any]]:
    """
    Make itinerary length match requested number of days.
    If itinerary is shorter, append free days.
    If longer, trim extra days.
    """
    updated_itinerary = deepcopy(itinerary)

    if len(updated_itinerary) > days:
        updated_itinerary = updated_itinerary[:days]

    while len(updated_itinerary) < days:
        updated_itinerary.append({
            "day": len(updated_itinerary) + 1,
            "activities": ["Free exploration"]
        })

    return updated_itinerary


def _reduce_cost(total_cost: float, budget: float) -> float:
    """
    Reduce total cost down to budget if exceeded.
    """
    if total_cost > budget:
        return budget
    return total_cost


def recommendation_agent(state: TravelState) -> TravelState:
    state["logs"].append(log_event("Recommendation Agent", "Recommendation step started"))

    state["recommendation_attempts"] = state.get("recommendation_attempts", 0) + 1

    if state.get("validation_status") != "INVALID":
        state["logs"].append(
            log_event("Recommendation Agent", "Plan already valid, no recommendation needed")
        )
        return state

    recommended_changes: List[str] = []
    updated_itinerary = deepcopy(state.get("itinerary", []))
    updated_total_cost = state.get("total_cost", 0.0)

    validation_errors = state.get("validation_errors", [])
    budget = state.get("budget", 0.0)
    days = state.get("days", 0)

    for error in validation_errors:
        error_lower = error.lower()

        if "budget exceeded" in error_lower:
            # Reduce itinerary complexity instead of only changing total_cost
            updated_itinerary = _reduce_activities(updated_itinerary, max_activities_per_day=1)
            recommended_changes.append("Reduced number of paid activities to lower the total cost.")

        if "too many activities" in error_lower:
            updated_itinerary = _reduce_activities(updated_itinerary, max_activities_per_day=2)
            recommended_changes.append("Reduced number of activities per day.")

        if "no activities" in error_lower:
            updated_itinerary = _fill_empty_days(updated_itinerary)
            recommended_changes.append("Filled empty days with a simple low-cost activity.")

        if "day count mismatch" in error_lower:
            updated_itinerary = _match_day_count(updated_itinerary, days)
            recommended_changes.append("Adjusted itinerary to match requested number of days.")

    state["itinerary"] = updated_itinerary
    state["recommended_changes"] = recommended_changes

    final_output = {
        "destination": state.get("destination"),
        "days": state.get("days"),
        "budget": state.get("budget"),
        "preferences": state.get("preferences"),
        "itinerary": state.get("itinerary"),
        "cost_breakdown": state.get("cost_breakdown"),
        "total_cost": state.get("total_cost"),
        "validation_status": "RECOMMENDED",
        "validation_errors": state.get("validation_errors"),
        "recommended_changes": state.get("recommended_changes")
    }

    output_filename = f"{state.get('destination', 'trip').lower()}_recommended_plan.json"
    output_file = write_itinerary_to_file(final_output, output_filename)
    state["output_file"] = output_file

    state["logs"].append(
        log_event("Recommendation Agent", f"Recommendation complete. Output saved to {output_file}")
    )

    return state