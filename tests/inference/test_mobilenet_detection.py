"""Tests mobilenet inference object on jetson devices."""
from peernet.inference.JetsonInference import MobileNetV2


def test_mobilenet_construction():
    """Can't really test anything other than construction without sampling."""
    try:
        _ = MobileNetV2()
        assert True

    except:  # noqa: E722
        assert False
