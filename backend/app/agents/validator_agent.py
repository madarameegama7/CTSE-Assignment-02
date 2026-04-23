from pathlib import Path

from app.graph.state import TravelState
from app.tools.validate_constraints import validate_constraints
from app.utils.logger import log_event


def _load_validator_prompt() -> str:
    """
    Load the validator agent prompt from the prompts directory.

    Returns:
        Prompt text as a string.

    Raises:
        FileNotFoundError: If the prompt file does not exist.
    """
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "validator_prompt.txt"
    return prompt_path.read_text(encoding="utf-8").strip()


def validator_agent(state: TravelState) -> TravelState:
    """
    Validate the travel plan stored in shared state.

    Runtime design note:
    - The validator agent uses its prompt file as an agent contract.
    - Actual validation is deterministic and tool-based to reduce hallucinations.
    - This preserves strong reliability while still honoring the required
      prompt/persona/constraints design for the agent.

    Updates:
    - validation_status
    - validation_errors
    - logs
    """
    logs = list(state.get("logs", []))
    logs.append(log_event("Validator Agent", "Validation started"))

    try:
        prompt_text = _load_validator_prompt()
        logs.append(
            log_event(
                "Validator Agent",
                "Validator contract loaded from validator_prompt.txt in deterministic mode",
            )
        )
        state["validator_prompt_contract"] = prompt_text
    except FileNotFoundError as exc:
        logs.append(
            log_event("Validator Agent", f"Validator prompt file missing: {exc}")
        )
        state["validator_prompt_contract"] = ""

    result = validate_constraints(
        itinerary=state.get("itinerary", []),
        total_cost=state.get("total_cost", 0.0),
        budget=state.get("budget", 0.0),
        days=state.get("days", 0),
    )

    state["validation_status"] = result["validation_status"]
    state["validation_errors"] = result["validation_errors"]

    if result["validation_status"] == "VALID":
        logs.append(
            log_event("Validator Agent", "Plan validated successfully")
        )
    else:
        logs.append(
            log_event(
                "Validator Agent",
                f"Plan invalid: {'; '.join(result['validation_errors'])}",
            )
        )

    state["logs"] = logs
    return state