from __future__ import annotations

from typing import Any, Dict

import pytest

import app.agents.planner_agent as planner_agent
from app.tools.data_reader import (
    format_destination_context,
    normalize_destination_key,
    read_destination_data,
)


class DummyResponse:
    """Simple fake LLM response object."""

    def __init__(self, content: str) -> None:
        self.content = content


class DummyLLM:
    """Fake LLM used to make planner tests deterministic."""

    def invoke(self, messages: Any) -> DummyResponse:
        combined_text = str(messages)

        assert "Ella" in combined_text
        assert "Days: 2" in combined_text
        assert "nature, hiking" in combined_text
        assert "Nine Arch Bridge" in combined_text

        return DummyResponse(
            "Initial Trip Draft\n"
            "Destination: Ella\n"
            "Duration: 2 days\n\n"
            "Draft Itinerary\n"
            "Day 1:\n"
            "- Nine Arch Bridge\n"
            "- Ravana Falls\n\n"
            "Day 2:\n"
            "- Little Adam's Peak\n"
            "- Ella Rock\n\n"
            "Planning Notes:\n"
            "- Generated from local destination data."
        )


@pytest.fixture
def sample_state() -> Dict[str, Any]:
    """Shared planner state used across tests."""
    return {
        "destination": "Ella",
        "days": 2,
        "budget": 400.0,
        "preferences": ["nature", "hiking"],
        "itinerary": [],
        "planner_output": "",
        "cost_breakdown": {},
        "total_cost": 0.0,
        "validation_status": "PENDING",
        "validation_errors": [],
        "recommended_changes": [],
        "output_file": None,
        "logs": [],
    }


def test_normalize_destination_key() -> None:
    assert normalize_destination_key("Ella") == "ella"
    assert normalize_destination_key("Nuwara Eliya") == "nuwara_eliya"


def test_read_destination_data_for_known_destination() -> None:
    result = read_destination_data("Ella")

    assert result["destination"] == "Ella"
    assert result["found"] is True
    assert "Nine Arch Bridge" in result["must_see_places"]
    assert "activities" in result


def test_format_destination_context_contains_expected_content() -> None:
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


def test_select_activities_returns_structured_itinerary() -> None:
    destination_data = read_destination_data("Ella")

    itinerary = planner_agent._select_activities(
        destination_data=destination_data,
        preferences=["nature", "hiking"],
        days=2,
        max_activities_per_day=2,
    )

    assert isinstance(itinerary, list)
    assert len(itinerary) == 2
    assert itinerary[0]["day"] == 1
    assert isinstance(itinerary[0]["activities"], list)


def test_build_planner_user_message_contains_required_fields() -> None:
    destination_data = read_destination_data("Ella")
    itinerary = [
        {"day": 1, "activities": ["Nine Arch Bridge", "Ravana Falls"]},
        {"day": 2, "activities": ["Little Adam's Peak", "Ella Rock"]},
    ]

    message = planner_agent._build_planner_user_message(
        destination="Ella",
        days=2,
        travelers=1,
        preferences=["nature", "hiking"],
        destination_data=destination_data,
        itinerary=itinerary,
    )

    assert "Destination: Ella" in message
    assert "Days: 2" in message
    assert "nature, hiking" in message
    assert "Nine Arch Bridge" in message
    assert "Structured itinerary draft" in message


def test_planner_agent_updates_state_with_llm_output(
    monkeypatch: pytest.MonkeyPatch,
    sample_state: Dict[str, Any],
) -> None:
    monkeypatch.setattr(planner_agent, "get_llm", lambda: DummyLLM())
    monkeypatch.setattr(planner_agent, "_load_planner_prompt", lambda: "Planner prompt")

    updated_state = planner_agent.planner_agent(sample_state)

    assert len(updated_state["itinerary"]) == 2
    assert updated_state["planner_output"] != ""
    assert "Initial Trip Draft" in updated_state["planner_output"]
    assert any("Planner Agent" in message for message in updated_state["logs"])


def test_planner_agent_falls_back_when_llm_fails(
    monkeypatch: pytest.MonkeyPatch,
    sample_state: Dict[str, Any],
) -> None:
    class FailingLLM:
        def invoke(self, messages: Any) -> DummyResponse:
            raise RuntimeError("Ollama not available")

    monkeypatch.setattr(planner_agent, "get_llm", lambda: FailingLLM())
    monkeypatch.setattr(planner_agent, "_load_planner_prompt", lambda: "Planner prompt")

    updated_state = planner_agent.planner_agent(sample_state)

    assert len(updated_state["itinerary"]) == 2
    assert "Initial Trip Draft" in updated_state["planner_output"]
    assert "Draft Itinerary" in updated_state["planner_output"]
    assert any("fallback" in message.lower() for message in updated_state["logs"])