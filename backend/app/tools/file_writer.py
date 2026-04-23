import json
from pathlib import Path
from typing import Any, Dict


OUTPUT_DIR = Path("outputs/itineraries")


def write_itinerary_to_file(data: Dict[str, Any], filename: str = "final_plan.json") -> str:
    """
    Save the final travel plan to a JSON file.

    Args:
        data: Final itinerary/state data to save.
        filename: Name of the output file.

    Returns:
        The file path as a string.

    Raises:
        TypeError: If data is not a dictionary.
        ValueError: If filename is empty.
    """
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    if not filename or not isinstance(filename, str):
        raise ValueError("filename must be a non-empty string")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_path = OUTPUT_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return str(file_path)