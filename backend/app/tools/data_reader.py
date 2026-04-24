from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "destinations.json"


def normalize_destination_key(destination: str) -> str:
    """
    Convert a destination name into a normalized key used in destinations.json.

    Example:
        "Nuwara Eliya" -> "nuwara_eliya"

    Args:
        destination: Raw destination text.

    Returns:
        Normalized destination key.

    Raises:
        ValueError: If destination is empty or only whitespace.
    """
    cleaned = destination.strip().lower()
    if not cleaned:
        raise ValueError("Destination cannot be empty.")

    return cleaned.replace(" ", "_")


def read_destination_data(destination: str) -> Dict[str, Any]:
    """
    Read destination data from the single JSON dataset file.

    Args:
        destination: Destination name such as 'Ella' or 'Kandy'.

    Returns:
        A dictionary of destination details. If the destination is not found,
        a safe fallback dictionary is returned.

    Raises:
        ValueError: If destination is empty.
        FileNotFoundError: If the dataset file does not exist.
        json.JSONDecodeError: If the JSON file is malformed.
    """
    key = normalize_destination_key(destination)

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Destination data file not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8") as file:
        all_destinations: Dict[str, Any] = json.load(file)

    if key not in all_destinations:
        return {
            "destination": destination.strip(),
            "found": False,
            "summary": "No local destination data found. Use only cautious planning assumptions.",
            "areas_to_stay": [],
            "transport_tips": [],
            "must_see_places": [],
            "food_notes": []
        }

    destination_data = dict(all_destinations[key])
    destination_data["found"] = True
    return destination_data


def format_destination_context(destination_data: Dict[str, Any]) -> str:
    """
    Convert structured destination data into a formatted text block for the planner prompt.

    Args:
        destination_data: Destination dictionary from read_destination_data().

    Returns:
        A readable text block for prompt injection.
    """
    destination = destination_data.get("destination", "Unknown")
    summary = destination_data.get("summary", "No summary available.")
    areas_to_stay = destination_data.get("areas_to_stay", [])
    transport_tips = destination_data.get("transport_tips", [])
    must_see_places = destination_data.get("must_see_places", [])
    food_notes = destination_data.get("food_notes", [])
    found = destination_data.get("found", False)

    return (
        f"Destination found in local dataset: {found}\n"
        f"Destination: {destination}\n"
        f"Summary: {summary}\n"
        f"Areas to stay: {', '.join(areas_to_stay) if areas_to_stay else 'N/A'}\n"
        f"Transport tips: {', '.join(transport_tips) if transport_tips else 'N/A'}\n"
        f"Must-see places: {', '.join(must_see_places) if must_see_places else 'N/A'}\n"
        f"Food notes: {', '.join(food_notes) if food_notes else 'N/A'}"
    )


# --- Cost and Destination Data Loaders ---

COSTS_FILE = BASE_DIR / "data" / "costs.json"


def load_costs() -> Dict[str, Any]:
    """
    Load cost data from the costs JSON file.

    Returns:
        A dictionary mapping destination names to cost information.

    Raises:
        FileNotFoundError: If the costs file does not exist.
        json.JSONDecodeError: If the JSON file is malformed.
    """
    if not COSTS_FILE.exists():
        raise FileNotFoundError(f"Costs data file not found: {COSTS_FILE}")

    with COSTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_destinations() -> Dict[str, Any]:
    """
    Load all destination data from the destinations JSON file.

    Returns:
        A dictionary mapping normalized destination keys to destination data.

    Raises:
        FileNotFoundError: If the destinations file does not exist.
        json.JSONDecodeError: If the JSON file is malformed.
    """
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Destination data file not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)