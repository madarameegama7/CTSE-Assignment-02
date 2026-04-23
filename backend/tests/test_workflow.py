import os

from app.models.request_models import TripRequest
from app.graph.workflow import run_travel_workflow


def test_workflow_generates_complete_result():
    request = TripRequest(
        destination="Ella",
        days=2,
        budget=400,
        preferences=["nature"]
    )

    result = run_travel_workflow(request)

    assert result["destination"] == "Ella"
    assert result["days"] == 2
    assert result["budget"] == 400
    assert isinstance(result["itinerary"], list)
    assert len(result["itinerary"]) == 2
    assert isinstance(result["planner_output"], str)
    assert isinstance(result["cost_breakdown"], dict)
    assert isinstance(result["logs"], list)
    assert result["validation_status"] in ["VALID", "INVALID"]
    assert result["output_file"] is not None
    assert os.path.exists(result["output_file"])


def test_workflow_triggers_invalid_or_recommendation_path():
    request = TripRequest(
        destination="Ella",
        days=2,
        budget=50,
        preferences=["nature"]
    )

    result = run_travel_workflow(request)

    assert result["validation_status"] == "INVALID"
    assert isinstance(result["logs"], list)
    assert any(
        "Recommendation Agent" in message or "Maximum recommendation attempts" in message
        for message in result["logs"]
    )