from __future__ import annotations

from typing import Any, Dict

import pytest

from agents import planner_agent
from tools.data_reader import (
    format_destination_context,
    normalize_destination_key,
    read_destination_data,
)

# --- Mock Objects for Testing ---

class DummyResponse:
    """
    Simple fake response object that mimics an LLM response structure.
    Used to simulate the output of an LLM call.
    """

    def __init__(self, content: str) -> None:
        self.content = content


class DummyLLM:
    """
    Simple fake LLM for deterministic planner tests.
    Overrides the invoke method to return a predefined response and verify input messages.
    """

    def invoke(self, messages: Any) -> DummyResponse:
        combined_text = str(messages)

        # Basic validation to ensure the planner node is passing expected data to the LLM
        assert "Ella" in combined_text
        assert "scenic views" in combined_text
        assert "Local destination data" in combined_text
        assert "Nine Arch Bridge" in combined_text

        # Return a mock response that matches the expected planner output format
        return DummyResponse(
            "Initial Trip Draft\n"
            "Destination: Ella\n"
            "Duration: 3 days\n"
            "Travelers: 2\n"
            "Interests: scenic views, hiking, cafes\n"
            "Assumptions: Moderate walking is acceptable.\n\n"
            "Draft Itinerary\n"
            "Day 1:\n"
            "- Morning: Visit Nine Arch Bridge\n"
            "- Afternoon: Relax at a cafe in Ella Town\n"
            "- Evening: Easy local walk\n\n"
            "Planning Notes for Budget Agent:\n"
            "- Estimate transport and meal costs.\n\n"
            "Planning Notes for Constraint and Validation Agent:\n"
            "- Check whether hiking load is too high.\n\n"
            "Planning Notes for Recommendation Agent:\n"
            "- Add optional hidden-gem activities."
        )


# --- Pytest Fixtures ---

@pytest.fixture
def sample_state() -> Dict[str, Any]:
    """
    Shared sample planner state for tests.
    Represents the initial state passed into the planner agent.
    """
    return {
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


# --- Unit Tests ---

def test_normalize_destination_key() -> None:
    """
    Test destination key normalization logic.
    Ensures that city names are correctly formatted for local data lookups.
    """
    assert normalize_destination_key("Ella") == "ella"
    assert normalize_destination_key("Nuwara Eliya") == "nuwara_eliya"


def test_read_destination_data_for_known_destination() -> None:
    """
    Test reading a known Sri Lankan destination from the JSON dataset.
    Verifies that we can successfully fetch data for a valid destination.
    """
    result = read_destination_data("Ella")

    assert result["destination"] == "Ella"
    assert result["found"] is True
    assert "Nine Arch Bridge" in result["must_see_places"]


def test_format_destination_context_contains_expected_content() -> None:
    """
    Test conversion of destination data dictionary into a readable string prompt context.
    Ensures that all key information is present in the final prompt string.
    """
    data = {
        "destination": "Kandy",
        "summary": "A cultural city.",
        "areas_to_stay": ["Kandy City Center"],
        "transport_tips": ["Use tuk-tuks"],
        "must_see_places": ["Temple of the Tooth"],
        "food_notes": ["Try rice and curry"],
        "found": True,
    }

    context = format_destination_context(data)

    assert "Destination: Kandy" in context
    assert "Temple of the Tooth" in context
    assert "Destination found in local dataset: True" in context


def test_build_planner_input_includes_required_fields(sample_state: Dict[str, Any]) -> None:
    """
    Test that the planner input string includes user requirements and destination context.
    Verifies that the planner receives all necessary information to create a plan.
    """
    planner_input = planner_agent.build_planner_input(sample_state)

    assert "Ella" in planner_input
    assert "relaxed and budget-conscious" in planner_input
    assert "Keep the plan realistic and not too tiring." in planner_input
    assert "Nine Arch Bridge" in planner_input


def test_planner_agent_updates_state(monkeypatch: pytest.MonkeyPatch, sample_state: Dict[str, Any]) -> None:
    """
    Test that the planner node correctly updates the shared state.
    1. Mocks the LLM to provide deterministic output.
    2. Runs the planner agent.
    3. Verifies that output fields (planner_output, draft_itinerary) are populated.
    4. Verifies that the current_stage is moved to 'budget_agent'.
    """
    # Mock the external dependencies (LLM and Prompt Loader)
    monkeypatch.setattr(planner_agent, "ChatOllama", lambda model, temperature: DummyLLM())
    monkeypatch.setattr(planner_agent, "load_planner_prompt", lambda prompt_path="prompts/planner_prompt.txt": "Planner prompt")

    planner_node = planner_agent.create_planner_agent()
    updated_state = planner_node(sample_state)

    # Assertions to verify state updates and state machine transitions
    assert updated_state["planner_status"] == "completed"
    assert updated_state["planner_model"] == "qwen2.5:3b"
    assert updated_state["current_stage"] == "budget_agent"
    assert "Initial Trip Draft" in updated_state["planner_output"]
    assert "Visit Nine Arch Bridge" in updated_state["draft_itinerary"]