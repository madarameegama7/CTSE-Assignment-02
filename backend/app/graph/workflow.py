from langgraph.graph import StateGraph, END

from app.graph.state import TravelState
from app.models.request_models import TripRequest
from app.utils.logger import log_event
from app.tools.file_writer import write_itinerary_to_file

from app.agents.planner_agent import planner_agent
from app.agents.budget_agent import run_budget_agent
from app.agents.validator_agent import validator_agent
from app.agents.recommendation_agent import recommendation_agent


def _build_initial_state(request: TripRequest) -> TravelState:
    return {
        "destination": request.destination,
        "days": request.days,
        "budget": request.budget,
        "preferences": request.preferences,
        "itinerary": [],
        "planner_output": "",
        "cost_breakdown": {},
        "total_cost": 0.0,
        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "recommendation_attempts": 0,
        "logs": [log_event("System", "Workflow started")]
    }


def _route_after_validation(state: TravelState) -> str:
    if state.get("validation_status") == "INVALID":
        attempts = state.get("recommendation_attempts", 0)

        if attempts >= 1:
            state["logs"].append(
                log_event("System", "Maximum recommendation attempts reached, ending workflow")
            )
            return "end"

        state["logs"].append(log_event("System", "Routing to Recommendation Agent"))
        return "recommendation"

    state["logs"].append(log_event("System", "Validation passed, ending workflow"))
    return "end"


def build_travel_graph():
    graph_builder = StateGraph(TravelState)

    graph_builder.add_node("planner", planner_agent)
    graph_builder.add_node("budget", run_budget_agent)
    graph_builder.add_node("validator", validator_agent)
    graph_builder.add_node("recommendation", recommendation_agent)

    graph_builder.set_entry_point("planner")

    graph_builder.add_edge("planner", "budget")
    graph_builder.add_edge("budget", "validator")

    graph_builder.add_conditional_edges(
        "validator",
        _route_after_validation,
        {
            "recommendation": "recommendation",
            "end": END,
        },
    )

    graph_builder.add_edge("recommendation", "budget")

    return graph_builder.compile()


travel_graph = build_travel_graph()


def _save_final_output(state: TravelState) -> TravelState:
    """
    Save the final workflow result only after final budget calculation
    and final validation have completed.
    """
    final_output = {
        "destination": state.get("destination"),
        "days": state.get("days"),
        "budget": state.get("budget"),
        "preferences": state.get("preferences"),
        "itinerary": state.get("itinerary"),
        "planner_output": state.get("planner_output"),
        "cost_breakdown": state.get("cost_breakdown"),
        "total_cost": state.get("total_cost"),
        "validation_status": state.get("validation_status"),
        "validation_errors": state.get("validation_errors"),
        "recommended_changes": state.get("recommended_changes"),
        "recommendation_attempts": state.get("recommendation_attempts"),
    }

    output_filename = f"{str(state.get('destination', 'trip')).lower()}_final_plan.json"
    output_file = write_itinerary_to_file(final_output, output_filename)
    state["output_file"] = output_file
    state["logs"].append(log_event("System", f"Final output saved to {output_file}"))
    return state


def run_travel_workflow(request: TripRequest) -> TravelState:
    initial_state = _build_initial_state(request)
    final_state = travel_graph.invoke(initial_state)
    final_state = _save_final_output(final_state)
    final_state["logs"].append(log_event("System", "Workflow completed"))
    return final_state