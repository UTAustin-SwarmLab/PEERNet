"""Simple test to document overhead in measurement.

In hindsight, this test is not actually very useful, since time.sleep()
accuracy is questionable.
"""

from peernet.metrics import Timer
import time


def test_overhead():
    """Documents timing overhead."""
    t = Timer("root")
    for i in range(100):
        x = t.log_section(f"{i}")
        time.sleep(0.0001)
        x.end_collection()
    t.end_collection()

    print(t)
