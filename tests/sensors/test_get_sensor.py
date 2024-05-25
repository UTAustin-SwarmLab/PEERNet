"""Tests the functionality of sensors/get_sensor.py."""
from peernet.sensors import get_sensor
import pytest

def test_random_string():
    """Tests behavior of random_string sensor."""
    sensor = get_sensor("random string", None, None)
    for i in range(10):
        rs = sensor.sample(i)
        assert len(rs) == i

def test_fixed_image():
    """Tests behavior of fixed_image sensor."""
    sensor = get_sensor("image", "resources/test_image_dog.jpeg", None)
    sensor.sample()

def test_external():
    """Tests behavior of external sensor."""
    sensor = get_sensor("external", None, "dummy_sensor::ds")
    assert sensor.sample() == sensor.magic_number

    with pytest.raises(TypeError):
        _ = get_sensor("external", None, "dummy_sensor::dsw")

def test_wrong_sensor_type():
    """Ensures an invalid sensor type raises a ValueError."""
    with pytest.raises(ValueError):
        get_sensor("ThisTypeDoesn'tExist", None, None)