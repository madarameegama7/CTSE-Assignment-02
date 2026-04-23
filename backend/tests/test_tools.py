from app.tools.data_reader import load_destinations, load_costs


def test_load_destinations():
    data = load_destinations()
    assert "ella" in data
    assert "activities" in data["ella"]


def test_load_costs():
    data = load_costs()
    assert "ella" in data
    assert "hotel_per_night" in data["ella"]