from app.tools.data_reader import load_destinations, load_costs


def test_load_destinations():
    data = load_destinations()
    assert "Ella" in data
    assert "activities" in data["Ella"]


def test_load_costs():
    data = load_costs()
    assert "Ella" in data
    assert "hotel_per_night" in data["Ella"]