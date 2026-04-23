from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

from app.graph.state import TravelState
from app.utils.logger import log_event


def _load_recommendation_prompt() -> str:
    """
    Load the recommendation agent prompt from the prompts directory.

    Returns:
        Prompt text as a string.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "recommendation_prompt.txt"
    return prompt_path.read_text(encoding="utf-8").strip()


def _reduce_activities(
    itinerary: List[Dict[str, Any]],
    max_activities_per_day: int = 2,
) -> List[Dict[str, Any]]:
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
            "activities": ["Free exploration"],
        })

    return updated_itinerary


def recommendation_agent(state: TravelState) -> TravelState:
    """
    Improve an invalid travel plan by making conservative itinerary adjustments.

    Runtime design note:
    - The recommendation agent uses its prompt file as an agent contract.
    - Actual recommendation behavior is deterministic and rule-based so that
      changes remain explainable, safe, and easy to validate.

    Important:
    - This agent does NOT recalculate budget.
    - This agent does NOT save the final output file.
    - Budget recalculation happens in the next Budget Agent step.
    - Final validity is determined by the Validator Agent after recalculation.
    """
    logs = list(state.get("logs", []))
    logs.append(log_event("Recommendation Agent", "Recommendation step started"))

    try:
        prompt_text = _load_recommendation_prompt()
        logs.append(
            log_event(
                "Recommendation Agent",
                "Recommendation contract loaded from recommendation_prompt.txt in deterministic mode",
            )
        )
        state["recommendation_prompt_contract"] = prompt_text
    except FileNotFoundError as exc:
        logs.append(
            log_event("Recommendation Agent", f"Recommendation prompt file missing: {exc}")
        )
        state["recommendation_prompt_contract"] = ""

    state["recommendation_attempts"] = state.get("recommendation_attempts", 0) + 1

    if state.get("validation_status") != "INVALID":
        logs.append(
            log_event("Recommendation Agent", "Plan already valid, no recommendation needed")
        )
        state["logs"] = logs
        return state

    recommended_changes: List[str] = []
    updated_itinerary = deepcopy(state.get("itinerary", []))

    validation_errors = state.get("validation_errors", [])
    days = state.get("days", 0)

    for error in validation_errors:
        error_lower = error.lower()

        if "budget exceeded" in error_lower:
            updated_itinerary = _reduce_activities(updated_itinerary, max_activities_per_day=1)
            recommended_changes.append(
                "Reduced number of paid activities to help lower the total cost."
            )

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

    logs.append(
        log_event(
            "Recommendation Agent",
            "Recommendation complete. Updated itinerary sent to Budget Agent for recalculation",
        )
    )
    state["logs"] = logs

    return state