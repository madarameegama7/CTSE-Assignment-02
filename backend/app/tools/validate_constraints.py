from typing import Any, Dict, List


def validate_constraints(
    itinerary: List[Dict[str, Any]],
    total_cost: float,
    budget: float,
    days: int,
    max_activities_per_day: int = 3
) -> Dict[str, Any]:
    """
    Validate whether a generated travel itinerary satisfies the user's
    constraints such as budget, trip duration, and itinerary structure.

    Args:
        itinerary: A list of itinerary items. Each item should represent
            one day and contain at least:
            {
                "day": int,
                "activities": List[str]
            }
        total_cost: The total estimated trip cost.
        budget: The user's maximum allowed budget.
        days: The requested number of travel days.
        max_activities_per_day: Maximum allowed activities per day.

    Returns:
        A dictionary containing:
            - validation_status: "VALID" or "INVALID"
            - validation_errors: list of error messages

    Raises:
        TypeError: If input types are invalid.
        ValueError: If budget or days are negative/zero where not allowed.
    """
    if not isinstance(itinerary, list):
        raise TypeError("itinerary must be a list")

    if not isinstance(total_cost, (int, float)):
        raise TypeError("total_cost must be a number")

    if not isinstance(budget, (int, float)):
        raise TypeError("budget must be a number")

    if not isinstance(days, int):
        raise TypeError("days must be an integer")

    if days <= 0:
        raise ValueError("days must be greater than 0")

    if budget <= 0:
        raise ValueError("budget must be greater than 0")

    errors: List[str] = []

    if not itinerary:
        errors.append("Itinerary is empty.")

    if len(itinerary) != days:
        errors.append(
            f"Itinerary day count mismatch. Expected {days}, got {len(itinerary)}."
        )

    for index, day_plan in enumerate(itinerary, start=1):
        if not isinstance(day_plan, dict):
            errors.append(f"Day {index} is not a valid dictionary entry.")
            continue

        if "day" not in day_plan:
            errors.append(f"Day entry {index} is missing 'day' field.")

        if "activities" not in day_plan:
            errors.append(f"Day entry {index} is missing 'activities' field.")
            continue

        activities = day_plan["activities"]

        if not isinstance(activities, list):
            errors.append(f"Activities for day {index} must be a list.")
            continue

        if len(activities) == 0:
            errors.append(f"Day {index} has no activities planned.")

        if len(activities) > max_activities_per_day:
            errors.append(
                f"Day {index} has too many activities "
                f"({len(activities)} > {max_activities_per_day})."
            )

    if total_cost > budget:
        exceeded_by = total_cost - budget
        errors.append(
            f"Budget exceeded by {exceeded_by:.2f}. "
            f"Total cost is {total_cost:.2f}, budget is {budget:.2f}."
        )

    return {
        "validation_status": "VALID" if not errors else "INVALID",
        "validation_errors": errors
    }