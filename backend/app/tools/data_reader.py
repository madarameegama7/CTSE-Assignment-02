import json
from pathlib import Path
from typing import Dict, Any


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_destinations() -> Dict[str, Any]:
    file_path = DATA_DIR / "destinations.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_costs() -> Dict[str, Any]:
    file_path = DATA_DIR / "costs.json"
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)