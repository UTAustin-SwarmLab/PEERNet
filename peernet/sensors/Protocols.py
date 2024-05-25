"""Defines a sensor protocol for typing sensor objects."""

from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class Sensor(Protocol):
    """Protocol for sensors that all sensor objects should adhere to."""

    def sample(self, *args, **kwargs) -> Any: ...  # noqa: D102
