"""Contains a dummy sensor class for testing get_sensor."""


class DummySensor:
    """Dummy Sensor for get_sensor test case to test external import."""

    def __init__(self) -> None:  # noqa: D107
        self.magic_number = 5

    def sample(self):
        """Returns magic number, verified in the test case."""
        return self.magic_number

class DummySensorWrong:
    """Dummy Sensor with incorrect sample() method name."""

    def __init__(self) -> None:  # noqa: D107
        self.magic_number = 5

    def get_sample(self):
        """Returns magic number, verified in the test case."""
        return self.magic_number

ds = DummySensor()
dsw = DummySensorWrong()
