import os
import pytest

from app.tools.file_writer import write_itinerary_to_file


def test_write_itinerary_to_file():
    data = {
        "destination": "Ella",
        "days": 2,
        "itinerary": []
    }

    path = write_itinerary_to_file(data, "test_output.json")

    assert os.path.exists(path)


def test_write_itinerary_to_file_invalid_data():
    with pytest.raises(TypeError):
        write_itinerary_to_file(["not", "a", "dict"], "bad.json")