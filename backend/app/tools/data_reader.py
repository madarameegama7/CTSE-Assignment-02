from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


DATA_FILE = Path("data/destinations.json")


def read_destination_data(destination: str) -> Dict[str, Any]:
    """
    Read destination data from a single JSON file.

    Args:
        destination: Name of the destination.

    Returns:
        Dictionary with destination details.
    """
    cleaned = destination.strip().lower()

    if not cleaned:
        raise ValueError("Destination cannot be empty")

    if not DATA_FILE.exists():
        raise FileNotFoundError("destinations.json file not found")

    with DATA_FILE.open("r", encoding="utf-8") as f:
        all_data = json.load(f)

    if cleaned not in all_data:
        return {
            "destination": destination,
            "found": False,
            "summary": "No data found. Use general knowledge carefully.",
            "areas_to_stay": [],
            "transport_tips": [],
            "must_see_places": [],
            "food_notes": []
        }

    data = all_data[cleaned]
    data["found"] = True
    return data


def format_destination_context(data: Dict[str, Any]) -> str:
    """
    Convert destination data to readable text.
    """
    return (
        f"Destination: {data.get('destination')}\n"
        f"Summary: {data.get('summary')}\n"
        f"Areas to stay: {', '.join(data.get('areas_to_stay', []))}\n"
        f"Transport tips: {', '.join(data.get('transport_tips', []))}\n"
        f"Must-see places: {', '.join(data.get('must_see_places', []))}\n"
        f"Food notes: {', '.join(data.get('food_notes', []))}"
    )