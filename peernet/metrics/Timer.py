"""Implementation of a subclass of MetricLogger for timing operations.

The timer subclass of MetricLogger is used to time operations. The metric it
tracks is elapsed time between calls to start and end.
"""

from peernet.metrics.MetricLogger import MetricLogger
import time


class Timer(MetricLogger):
    """A specific metric class for a timer that tracks latency measurements."""

    def __init__(self, name, depth=0):  # noqa: D107
        super().__init__(name, depth)
        self.metric_name = "Time"

    def _tic(self):
        self.start = time.time()

    def _toc(self):
        return time.time() - self.start


class Timing:
    """A context manager that wraps user-defined behavior with timing.

    __enter__() and ___exit__() mirror start and end collection.
    """

    def __init__(self, parent: MetricLogger, name: str):  # noqa: D107
        self.parent = parent
        self.name = name

    def __enter__(self):  # noqa: D105
        # Enter mirrors start_collection by opening a new section.
        self.section = self.parent.log_section(self.name, Timer)
        return self.section

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: D105
        # Exit mirrors end_collection, effectively stopping the timer.
        self.section.end_collection()
