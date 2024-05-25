"""Tests the context manager for timing a custom function call."""

from peernet.metrics import (
    Timer,  # noqa: F401
    Timing,
    TokensPerSecondMeter,  # noqa: F401
    TPSTracking,
    Container,
    ContainerNode,
    Value,  # noqa: F401
    ValueNode,
)
import time


def custom_func():  # noqa: D103
    time.sleep(0.5)


def test_context_managers_simple():
    """Tests simple performance of context managers."""
    print("\n")
    t = Container("root")

    with Timing(t, "sub-timer"):
        custom_func()

    with TPSTracking(t, "sub-tps") as tps:
        custom_func()
        tps.end_collection(10)

    with ContainerNode(t, "sub-container"):
        custom_func()

    with ValueNode(t, "sub-value") as vn:
        custom_func()
        vn.end_collection("Value of Value Node")

    print(t)
