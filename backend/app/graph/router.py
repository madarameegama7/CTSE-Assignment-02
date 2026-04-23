from app.graph.state import TravelState


def should_recommend(state: TravelState) -> str:
    if state.get("validation_status") == "INVALID":
        return "recommendation"
    return "end"