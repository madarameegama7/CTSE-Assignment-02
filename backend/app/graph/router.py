def should_recommend(state: dict) -> str:
    if state.get("validation_status") == "INVALID":
        return "recommendation"
    return "end"