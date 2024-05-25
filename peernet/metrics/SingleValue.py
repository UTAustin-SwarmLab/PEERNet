"""A subclass of MetricLogger designed to track single values.

This implementation of a logger is useful for tracking arbitrary custom
metrics that are easily computed. For example, use cases of the SingleValue
MetricLogger subclass can track the output of a model, debugging information,
or user-computed metrics without implementing a custom subclass.
"""

from peernet.metrics.MetricLogger import MetricLogger
from typing import Any


class Value(MetricLogger):
    """A subclass of Metric Logger designed to track a single value such as an integer, string, etc."""  # noqa: E501

    def __init__(self, name: str, depth: int = 0):  # noqa: D107
        super().__init__(name, depth)
        self.metric_name = "Value"

    def _tic(self):
        pass

    def _toc(self, value: Any):
        return value


class ValueNode:
    """Context Manager for Value subsections.

    Since context manager __exit__() methods cannot take auxiliary arguments,
    users are responsible for ending colelction even when using the ValueNode
    context manager.

    Example:
    >>> parent_logger = Container()
    >>> with ValueNode(parent_logger, "context-manager-node") as vn:
    >>>     #Do something
    >>>     vn.end_collection(computed_value)
    """

    def __init__(self, parent_logger: MetricLogger, name: str):  # noqa: D107
        self.parent = parent_logger
        self.name = name

    def __enter__(self):  # noqa: D105
        self.section = self.parent.log_section(self.name, Value)
        return self.section

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: D105
        # Manager exit requires nothing.
        pass
