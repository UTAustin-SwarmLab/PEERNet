"""Tests for fixed image dataset."""
from peernet.sensors.datasets import FixedImage

def test_fixed_image_sample():
    """Tests a FixedImage dataset by sampling and printing."""
    dataset = FixedImage("resources/test_image_dog.jpeg")

    sample = dataset.sample(numpy=True)

    print(sample)

    assert True