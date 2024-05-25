"""Container implementation of MetricLogger.

Containers are used strictly for organizational purposes. They represent events
that don't have associated metrics, but have sub-events. For example, iterations
in an experiment are represented using the Container. We also implement a context
manager for containers. See documentation for use of context managers for metrics.
"""

from peernet.metrics.MetricLogger import MetricLogger


class Container(MetricLogger):
    """Subclass of MetricLogger designed to maintain organization."""

    def __init__(self, name: str, depth: int = 0):  # noqa: D107
        super().__init__(name, depth)
        self.metric_name = "Container"
        self.metric = "No Metric"

    def _tic(self):
        """Tic method does nothing for container implementation."""
        pass

    def _toc(self):
        """Toc method returns string for debugging purposes."""
        return "No Metric"


class ContainerNode:
    """Context manager for simplifying syntax of using a Container in logging trees."""

    def __init__(self, parent: MetricLogger, name: str):  # noqa: D107
        self.parent = parent
        self.name = name

    def __enter__(self):  # noqa: D105
        #On enter, just log a new section in the parent logger
        self.section = self.parent.log_section(self.name, Container)
        return self.section

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: D105
        #Container does nothing on exit
        pass
