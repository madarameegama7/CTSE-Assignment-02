from app.agents.recommendation_agent import recommendation_agent


def test_recommendation_agent_no_action_for_valid_plan():
    state = {
        "destination": "Ella",
        "days": 2,
        "budget": 400.0,
        "preferences": ["nature"],
        "itinerary": [
            {"day": 1, "activities": ["Nine Arch Bridge", "Tea Plantation"]},
            {"day": 2, "activities": ["Little Adam's Peak"]}
        ],
        "cost_breakdown": {},
        "total_cost": 300.0,
        "validation_status": "VALID",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = recommendation_agent(state)

    assert result["validation_status"] == "VALID"
    assert result["recommended_changes"] == []


def test_recommendation_agent_reduces_budget():
    state = {
        "destination": "Ella",
        "days": 2,
        "budget": 200.0,
        "preferences": ["nature"],
        "itinerary": [
            {"day": 1, "activities": ["Nine Arch Bridge", "Tea Plantation"]},
            {"day": 2, "activities": ["Little Adam's Peak", "Ravana Falls"]}
        ],
        "cost_breakdown": {},
        "total_cost": 350.0,
        "validation_status": "INVALID",
        "validation_errors": [
            "Budget exceeded by 150.00. Total cost is 350.00, budget is 200.00."
        ],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = recommendation_agent(state)

    assert result["total_cost"] == 200.0
    assert any("budget" in change.lower() for change in result["recommended_changes"])
    assert result["output_file"] is not None


def test_recommendation_agent_reduces_too_many_activities():
    state = {
        "destination": "Ella",
        "days": 1,
        "budget": 500.0,
        "preferences": ["nature"],
        "itinerary": [
            {"day": 1, "activities": ["A", "B", "C", "D"]}
        ],
        "cost_breakdown": {},
        "total_cost": 150.0,
        "validation_status": "INVALID",
        "validation_errors": [
            "Day 1 has too many activities (4 > 3)."
        ],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = recommendation_agent(state)

    assert len(result["itinerary"][0]["activities"]) == 2
    assert any("activities" in change.lower() for change in result["recommended_changes"])


def test_recommendation_agent_fills_empty_day():
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
        "validation_status": "INVALID",
        "validation_errors": [
            "Day 1 has no activities planned."
        ],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = recommendation_agent(state)

    assert result["itinerary"][0]["activities"] == ["Free exploration"]
    assert any("empty days" in change.lower() or "filled" in change.lower() for change in result["recommended_changes"])


def test_recommendation_agent_fixes_day_count():
    state = {
        "destination": "Ella",
        "days": 3,
        "budget": 500.0,
        "preferences": ["nature"],
        "itinerary": [
            {"day": 1, "activities": ["A"]},
            {"day": 2, "activities": ["B"]}
        ],
        "cost_breakdown": {},
        "total_cost": 150.0,
        "validation_status": "INVALID",
        "validation_errors": [
            "Itinerary day count mismatch. Expected 3, got 2."
        ],
        "recommended_changes": [],
        "output_file": None,
        "logs": []
    }

    result = recommendation_agent(state)

    assert len(result["itinerary"]) == 3
    assert result["itinerary"][2]["activities"] == ["Free exploration"]
    assert any("day" in change.lower() for change in result["recommended_changes"])