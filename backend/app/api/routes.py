from fastapi import APIRouter
from app.models.request_models import TripRequest
from app.models.response_models import TripResponse
from app.graph.workflow import run_travel_workflow

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/plan-trip", response_model=TripResponse)
def plan_trip(request: TripRequest) -> TripResponse:
    result = run_travel_workflow(request)
    return TripResponse(**result)