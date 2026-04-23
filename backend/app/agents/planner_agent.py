from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Dict

from langchain_ollama import ChatOllama

from tools.data_reader import format_destination_context, read_destination_data


PlannerState = Dict[str, Any]


def setup_logger() -> logging.Logger:
    """
    Configure and return a file logger for planner agent observability.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("planner_agent")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        Path("logs").mkdir(exist_ok=True)
        handler = logging.FileHandler("logs/planner_agent.log", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logger()


def load_planner_prompt(prompt_path: str = "prompts/planner_prompt.txt") -> str:
    """
    Load the planner agent system prompt from a text file.

    Args:
        prompt_path: Path to the planner prompt file.

    Returns:
        Prompt text.

    Raises:
        FileNotFoundError: If prompt file does not exist.
    """
    path = Path(prompt_path)
    if not path.exists():
        raise FileNotFoundError(f"Planner prompt file not found: {prompt_path}")

    return path.read_text(encoding="utf-8")


def build_planner_input(state: PlannerState) -> str:
    """
    Build the text input passed to the planner model from shared state.

    Expected incoming state keys:
        - user_request
        - destination
        - days
        - travelers
        - interests
        - travel_style
        - special_notes

    Args:
        state: Shared multi-agent state.

    Returns:
        Structured planner input text.
    """
    user_request = state.get("user_request", "")
    destination = state.get("destination", "")
    days = state.get("days", "")
    travelers = state.get("travelers", "")
    interests = state.get("interests", [])
    travel_style = state.get("travel_style", "not specified")
    special_notes = state.get("special_notes", "No special notes provided.")

    destination_data = read_destination_data(destination)
    destination_context = format_destination_context(destination_data)

    interests_text = ", ".join(interests) if isinstance(interests, list) else str(interests)

    return (
        f"User travel request:\n{user_request}\n\n"
        f"Trip details:\n"
        f"- Destination: {destination}\n"
        f"- Number of days: {days}\n"
        f"- Number of travelers: {travelers}\n"
        f"- Interests: {interests_text}\n"
        f"- Travel style: {travel_style}\n"
        f"- Special notes: {special_notes}\n\n"
        f"Local destination data:\n{destination_context}\n"
    )


def create_planner_agent(
    model_name: str = "qwen2.5:3b",
    temperature: float = 0.2,
) -> Callable[[PlannerState], PlannerState]:
    """
    Create the Planner Agent callable.

    The returned function reads current shared state, generates an initial itinerary draft,
    and writes planner outputs back into shared state for downstream agents.

    Args:
        model_name: Ollama model name.
        temperature: Model temperature.

    Returns:
        Planner node callable.
    """
    llm = ChatOllama(model=model_name, temperature=temperature)
    system_prompt = load_planner_prompt()

    def planner_node(state: PlannerState) -> PlannerState:
        """
        Execute the Planner Agent.

        Added/updated state keys:
            - planner_output
            - draft_itinerary
            - planner_status
            - planner_model
            - current_stage

        Args:
            state: Shared workflow state.

        Returns:
            Updated shared state.
        """
        logger.info("Planner agent started.")
        logger.info("Incoming planner state: %s", state)

        planner_input = build_planner_input(state)

        messages = [
            ("system", system_prompt),
            ("human", planner_input),
        ]

        response = llm.invoke(messages)
        planner_output = response.content if hasattr(response, "content") else str(response)

        updated_state = dict(state)
        updated_state["planner_output"] = planner_output
        updated_state["draft_itinerary"] = planner_output
        updated_state["planner_status"] = "completed"
        updated_state["planner_model"] = model_name
        updated_state["current_stage"] = "budget_agent"

        logger.info("Planner agent completed successfully.")
        logger.info("Planner output: %s", planner_output)

        return updated_state

    return planner_node


if __name__ == "__main__":
    demo_state: PlannerState = {
        "user_request": (
            "Plan a 3-day trip to Ella for 2 friends who like scenic views, hiking, "
            "cafes, and relaxed travel."
        ),
        "destination": "Ella",
        "days": 3,
        "travelers": 2,
        "interests": ["scenic views", "hiking", "cafes"],
        "travel_style": "relaxed and budget-conscious",
        "special_notes": "Keep the plan realistic and not too tiring.",
    }

    planner = create_planner_agent()
    result = planner(demo_state)

    print("\n=== PLANNER AGENT OUTPUT ===\n")
    print(result["planner_output"])
    print("\n=== NEXT STAGE ===")
    print(result["current_stage"])