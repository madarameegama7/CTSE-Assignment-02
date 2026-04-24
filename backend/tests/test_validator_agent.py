from app.agents.validator_agent import validator_agent


def test_validator_agent_valid_plan():
    state = {
        "destination": "Ella",
        "days": 2,
        "budget": 400.0,
        "preferences": ["nature"],

        "itinerary": [
            {"day": 1, "activities": ["Nine Arch Bridge", "Tea Plantation"]},
            {"day": 2, "activities": ["Little Adam's Peak", "Ravana Falls"]}
        ],
        "cost_breakdown": {
            "hotel": 160.0,
            "food": 50.0,
            "transport": 60.0,
            "activities": 40.0
        },
        "total_cost": 310.0,

        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = validator_agent(state)

    assert result["validation_status"] == "VALID"
    assert result["validation_errors"] == []


def test_validator_agent_budget_exceeded():
    state = {
        "destination": "Ella",
        "days": 2,
        "budget": 200.0,
        "preferences": ["nature"],

        "itinerary": [
            {"day": 1, "activities": ["Nine Arch Bridge", "Tea Plantation"]},
            {"day": 2, "activities": ["Little Adam's Peak", "Ravana Falls"]}
        ],
        "cost_breakdown": {
            "hotel": 160.0,
            "food": 50.0,
            "transport": 60.0,
            "activities": 40.0
        },
        "total_cost": 310.0,

        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = validator_agent(state)

    assert result["validation_status"] == "INVALID"
    assert any("Budget exceeded" in error for error in result["validation_errors"])


def test_validator_agent_day_count_mismatch():
    state = {
        "destination": "Ella",
        "days": 3,
        "budget": 500.0,
        "preferences": ["nature"],

        "itinerary": [
            {"day": 1, "activities": ["Nine Arch Bridge"]},
            {"day": 2, "activities": ["Little Adam's Peak"]}
        ],
        "cost_breakdown": {},
        "total_cost": 200.0,

        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = validator_agent(state)

    assert result["validation_status"] == "INVALID"
    assert any("day count mismatch" in error.lower() for error in result["validation_errors"])


def test_validator_agent_empty_day_activities():
    state = {
        "destination": "Ella",
        "days": 2,
        "budget": 500.0,
        "preferences": ["nature"],

        "itinerary": [
            {"day": 1, "activities": []},
            {"day": 2, "activities": ["Ravana Falls"]}
        ],
        "cost_breakdown": {},
        "total_cost": 150.0,

        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = validator_agent(state)

    assert result["validation_status"] == "INVALID"
    assert any("no activities" in error.lower() for error in result["validation_errors"])