"""Tests performance of mixed children integration.

For ease-of-use, we allow MetricLoggers of one metric to contain nodes of other
MetricLogger types. This file tests integration of such "mixed children" trees.
"""

from peernet.metrics import (
    Timer,
    TokensPerSecondMeter,
    Value,
    Container,
)
import time


def test_multiple_types():
    """Tests construction of trees that have multiple children types."""
    print("\n")
    try:
        t = Container("root")

        for i in range(10):
            t_iter = t.log_section(f"{i}", Container)

            t_iter.log_section("inference-time", Timer)
            time.sleep(0.05)
            t_iter.end_sub("inference-time")

            t_iter.log_section("tps", TokensPerSecondMeter)
            time.sleep(0.05)
            t_iter.end_sub("tps", 50)

            t_iter.log_section("string", Value)
            t_iter.end_sub("string", "Hello")

        print(t)

        assert True
    except Exception:
        assert False


def test_multiple_types_csv():
    """Tests csv writing for mixed children trees."""
    print("\n")
    try:
        t = Container("root")

        for i in range(10):
            t_iter = t.log_section(f"{i}", Container)

            t_iter.log_section("inference-time", Timer)
            time.sleep(0.05)
            t_iter.end_sub("inference-time")

            t_iter.log_section("tps", TokensPerSecondMeter)
            time.sleep(0.05)
            t_iter.end_sub("tps", 50)

            t_iter.log_section("string", Value)
            t_iter.end_sub("string", "Hello")

        print(t)
        print(t.to_csv("ir.csv"))

        assert True
    except Exception:
        assert False
