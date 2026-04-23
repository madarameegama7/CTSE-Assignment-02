from __future__ import annotations

from typing import Any, Dict, List

from app.graph.state import TravelState
from app.tools.data_reader import read_destination_data
from app.utils.logger import log_event


def _select_activities(
    destination_data: Dict[str, Any],
    preferences: List[str],
    days: int,
    max_activities_per_day: int = 2
) -> List[Dict[str, Any]]:
    """
    Build a structured itinerary from local destination activities.

    The planner uses local dataset activities and tries to prefer activities
    whose type matches the user's preferences.
    """
    activities = destination_data.get("activities", [])
    if not isinstance(activities, list):
        activities = []

    normalized_preferences = [str(pref).strip().lower() for pref in preferences]

    matching = []
    non_matching = []

    for activity in activities:
        activity_type = str(activity.get("type", "")).strip().lower()
        if activity_type in normalized_preferences:
            matching.append(activity)
        else:
            non_matching.append(activity)

    ordered_activities = matching + non_matching

    itinerary: List[Dict[str, Any]] = []
    activity_index = 0

    for day in range(1, days + 1):
        day_activities: List[str] = []

        for _ in range(max_activities_per_day):
            if activity_index < len(ordered_activities):
                day_activities.append(ordered_activities[activity_index]["name"])
                activity_index += 1

        if not day_activities:
            day_activities = ["Free exploration"]

        itinerary.append({
            "day": day,
            "activities": day_activities
        })

    return itinerary


def _format_planner_output(
    destination: str,
    days: int,
    preferences: List[str],
    itinerary: List[Dict[str, Any]]
) -> str:
    """
    Create a human-readable planner summary from the structured itinerary.
    """
    lines = [
        "Initial Trip Draft",
        f"Destination: {destination}",
        f"Duration: {days} days",
        f"Preferences: {', '.join(preferences) if preferences else 'Not specified'}",
        "",
        "Draft Itinerary"
    ]

    for day_plan in itinerary:
        day_number = day_plan.get("day", "?")
        activities = day_plan.get("activities", [])
        lines.append(f"Day {day_number}:")
        for activity in activities:
            lines.append(f"- {activity}")
        lines.append("")

    return "\n".join(lines).strip()


def planner_agent(state: TravelState) -> TravelState:
    """
    Generate an initial structured itinerary using local destination data.

    Updates:
    - itinerary
    - planner_output
    - logs
    """
    logs = list(state.get("logs", []))
    logs.append(log_event("Planner Agent", "Planner started"))

    destination = state.get("destination", "")
    days = state.get("days", 0)
    preferences = state.get("preferences", [])

    destination_data = read_destination_data(destination)

    itinerary = _select_activities(
        destination_data=destination_data,
        preferences=preferences,
        days=days,
        max_activities_per_day=2
    )

    planner_output = _format_planner_output(
        destination=destination,
        days=days,
        preferences=preferences,
        itinerary=itinerary
    )

    state["itinerary"] = itinerary
    state["planner_output"] = planner_output
    state["logs"] = logs + [
        log_event("Planner Agent", f"Planner created itinerary for {days} day(s)")
    ]

    return state