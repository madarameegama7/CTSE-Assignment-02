from __future__ import annotations

from typing import Any, Dict, List

from app.graph.state import TravelState
from app.llm.ollama_client import get_llm
from app.tools.data_reader import read_destination_data
from app.utils.logger import log_event


def _load_planner_prompt() -> str:
    """
    Load the planner system prompt from file.
    """
    from pathlib import Path

    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "planner_prompt.txt"
    return prompt_path.read_text(encoding="utf-8")


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


def _build_planner_user_message(
    destination: str,
    days: int,
    preferences: List[str],
    destination_data: Dict[str, Any],
    itinerary: List[Dict[str, Any]]
) -> str:
    """
    Build grounded user input for the planner LLM.
    """
    summary = destination_data.get("summary", "No summary available.")
    areas_to_stay = destination_data.get("areas_to_stay", [])
    transport_tips = destination_data.get("transport_tips", [])

    itinerary_lines = []
    for day_plan in itinerary:
        day_number = day_plan.get("day", "?")
        activities = day_plan.get("activities", [])
        itinerary_lines.append(f"Day {day_number}: {', '.join(activities)}")

    return (
        f"Destination: {destination}\n"
        f"Days: {days}\n"
        f"Preferences: {', '.join(preferences) if preferences else 'Not specified'}\n\n"
        f"Local destination summary:\n{summary}\n\n"
        f"Suggested stay areas: {', '.join(areas_to_stay) if areas_to_stay else 'N/A'}\n"
        f"Transport tips: {', '.join(transport_tips) if transport_tips else 'N/A'}\n\n"
        f"Structured itinerary draft:\n" + "\n".join(itinerary_lines) + "\n\n"
        "Using only the grounded information above, write a short travel plan summary "
        "with a trip overview, the itinerary by day, and brief planning notes."
    )


def _fallback_planner_output(
    destination: str,
    days: int,
    preferences: List[str],
    itinerary: List[Dict[str, Any]]
) -> str:
    """
    Fallback planner output if Ollama is unavailable.
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

    lines.append("Planning Notes:")
    lines.append("- Generated from local destination data.")
    lines.append("- Budget and validation will be handled by downstream agents.")

    return "\n".join(lines).strip()


def planner_agent(state: TravelState) -> TravelState:
    """
    Generate an initial structured itinerary using local destination data,
    and produce a natural-language planner summary via Ollama.

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

    planner_output = ""

    try:
        llm = get_llm()
        system_prompt = _load_planner_prompt()
        user_message = _build_planner_user_message(
            destination=destination,
            days=days,
            preferences=preferences,
            destination_data=destination_data,
            itinerary=itinerary
        )

        response = llm.invoke([
            ("system", system_prompt),
            ("human", user_message),
        ])

        planner_output = response.content if hasattr(response, "content") else str(response)
        logs.append(log_event("Planner Agent", "Planner summary generated using Ollama"))

    except Exception as exc:
        planner_output = _fallback_planner_output(
            destination=destination,
            days=days,
            preferences=preferences,
            itinerary=itinerary
        )
        logs.append(log_event("Planner Agent", f"Ollama unavailable, using fallback output: {exc}"))

    state["itinerary"] = itinerary
    state["planner_output"] = planner_output
    state["logs"] = logs + [
        log_event("Planner Agent", f"Planner created itinerary for {days} day(s)")
    ]

    return state