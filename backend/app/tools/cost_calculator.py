from typing import Any, Dict, List

from app.tools.data_reader import load_costs, load_destinations, normalize_destination_key


def calculate_trip_cost(destination: str, days: int, itinerary: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate a structured cost estimate for a trip itinerary."""

    if not destination or not destination.strip():
        raise ValueError("Destination must be a non-empty string.")

    if days <= 0:
        raise ValueError("Days must be greater than zero.")

    if not isinstance(itinerary, list):
        raise ValueError("Itinerary must be a list of day plans.")

    # normalize destination
    destination_key = normalize_destination_key(destination)

    costs = load_costs()
    destinations = load_destinations()

    # use normalized key
    if destination_key not in costs:
        raise ValueError(f"No cost data found for destination: {destination}")

    if destination_key not in destinations:
        raise ValueError(f"No activity data found for destination: {destination}")

    destination_costs = costs[destination_key]

    activity_prices = {
        activity["name"]: float(activity.get("cost", 0.0))
        for activity in destinations[destination_key].get("activities", [])
    }

    accommodation_cost = float(destination_costs["hotel_per_night"]) * max(days - 1, 0)
    food_cost = float(destination_costs["food_per_day"]) * days
    transport_cost = float(destination_costs["transport_base"])
    activity_cost = _calculate_activity_cost(itinerary, activity_prices)

    cost_breakdown = {
        "accommodation": round(accommodation_cost, 2),
        "food": round(food_cost, 2),
        "transport": round(transport_cost, 2),
        "activities": round(activity_cost, 2),
    }

    total_cost = round(sum(cost_breakdown.values()), 2)

    return {
        "cost_breakdown": cost_breakdown,
        "total_cost": total_cost,
    }


def _calculate_activity_cost(itinerary: List[Dict[str, Any]], activity_prices: Dict[str, float]) -> float:
    """Return the total known activity cost from the itinerary."""
    total = 0.0

    for day_plan in itinerary:
        if not isinstance(day_plan, dict):
            raise ValueError("Each itinerary item must be a dictionary.")

        activities = day_plan.get("activities", [])
        if not isinstance(activities, list):
            raise ValueError("Each itinerary day must contain an activities list.")

        for activity_name in activities:
            if not isinstance(activity_name, str):
                raise ValueError("Activity names must be strings.")
            total += activity_prices.get(activity_name, 0.0)

    return total