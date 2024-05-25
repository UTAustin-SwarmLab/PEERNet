"""Tests TokensPerSecondMeter, an implementation of a metric."""

from peernet.metrics import TokensPerSecondMeter
import time


def test_simple():  # noqa: D103
    try:
        tps = TokensPerSecondMeter("tps")
        time.sleep(1)
        tps.end_collection(10)
        print(tps)
        assert True

    except Exception:
        assert False
