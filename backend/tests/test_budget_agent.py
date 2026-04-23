import pytest

from app.agents.budget_agent import run_budget_agent
from app.tools.cost_calculator import calculate_trip_cost


def _base_state() -> dict:
    return {
        "destination": "Ella",
        "days": 2,
        "budget": 400.0,
        "preferences": ["nature"],
        "itinerary": [
            {"day": 1, "activities": ["Nine Arch Bridge", "Ella Rock"]},
            {"day": 2, "activities": ["Little Adam's Peak", "Ravana Falls"]},
        ],
        "cost_breakdown": {},
        "total_cost": 0.0,
        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": [],
    }


def test_calculate_trip_cost_returns_breakdown_and_total():
    result = calculate_trip_cost(
        destination="Ella",
        days=2,
        itinerary=[
            {"day": 1, "activities": ["Nine Arch Bridge", "Ella Rock"]},
            {"day": 2, "activities": ["Little Adam's Peak", "Ravana Falls"]},
        ],
    )

    assert result["cost_breakdown"] == {
        "accommodation": 80.0,
        "food": 50.0,
        "transport": 60.0,
        "activities": 70.0,
    }
    assert result["total_cost"] == 260.0


def test_budget_agent_updates_state_without_changing_itinerary():
    state = _base_state()

    result = run_budget_agent(state)

    assert result["cost_breakdown"]["activities"] == 70.0
    assert result["total_cost"] == 260.0
    assert result["itinerary"] == state["itinerary"]
    assert any("[BudgetAgent]" in message for message in result["logs"])


def test_budget_agent_marks_state_invalid_when_destination_is_unknown():
    state = _base_state()
    state["destination"] = "Unknown City"

    result = run_budget_agent(state)

    assert result["validation_status"] == "INVALID"
    assert result["cost_breakdown"] == {}
    assert result["total_cost"] == 0.0
    assert any("Budget calculation error" in error for error in result["validation_errors"])


def test_calculate_trip_cost_rejects_unsafe_itinerary_shape():
    with pytest.raises(ValueError, match="activities list"):
        calculate_trip_cost(
            destination="Ella",
            days=2,
            itinerary=[{"day": 1, "activities": "Nine Arch Bridge"}],
        )