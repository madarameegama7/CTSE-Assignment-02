import pytest
from app.tools.validate_constraints import validate_constraints


def test_validate_constraints_valid():
    result = validate_constraints(
        itinerary=[
            {"day": 1, "activities": ["A", "B"]},
            {"day": 2, "activities": ["C"]}
        ],
        total_cost=300.0,
        budget=400.0,
        days=2
    )

    assert result["validation_status"] == "VALID"
    assert result["validation_errors"] == []


def test_validate_constraints_invalid_budget():
    result = validate_constraints(
        itinerary=[
            {"day": 1, "activities": ["A"]},
            {"day": 2, "activities": ["B"]}
        ],
        total_cost=500.0,
        budget=400.0,
        days=2
    )

    assert result["validation_status"] == "INVALID"
    assert any("Budget exceeded" in error for error in result["validation_errors"])


def test_validate_constraints_invalid_days():
    result = validate_constraints(
        itinerary=[
            {"day": 1, "activities": ["A"]}
        ],
        total_cost=100.0,
        budget=400.0,
        days=2
    )

    assert result["validation_status"] == "INVALID"
    assert any("Expected 2, got 1" in error for error in result["validation_errors"])


def test_validate_constraints_raises_for_invalid_days_value():
    with pytest.raises(ValueError):
        validate_constraints(
            itinerary=[],
            total_cost=0.0,
            budget=100.0,
            days=0
        )