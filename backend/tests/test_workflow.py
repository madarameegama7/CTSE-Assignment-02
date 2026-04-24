from app.models.request_models import TripRequest
from app.graph.workflow import run_travel_workflow


def test_workflow_initial_state():
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
    assert isinstance(result["logs"], list)