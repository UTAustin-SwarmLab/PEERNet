"""Implementation of a custom logger that tracks LLM output speed.

We measure speed in terms of TokensPerSecond outputted by the LLM. We implement
TokensPerSecondMeter, a subclass of MetricLogger, as a node type, and implement
TPSTracking as a context manager for tracking tokens per second
"""

from peernet.metrics.MetricLogger import MetricLogger
import time


class TokensPerSecondMeter(MetricLogger):
    """A specific metric class for a logger that tracks tokens per second from an LLM."""  # noqa: E501

    def __init__(self, name: str, depth=0):  # noqa: D107
        super().__init__(name, depth)
        self.metric_name = "Tokens Per Second"

    def _tic(self):
        self.start = time.time()

    def _toc(self, tokens):
        delta = time.time() - self.start
        return tokens / delta


class TPSTracking(MetricLogger):
    """A context manager that wraps user-defined behavior with TPS monitoring."""

    def __init__(self, parent: MetricLogger, name: str):  # noqa: D107
        self.parent = parent
        self.name = name

    def __enter__(self):  # noqa: D105
        self.section = self.parent.log_section(self.name, TokensPerSecondMeter)
        return self.section

    def __exit__(self, exc_type, exc_value, traceback):  # noqa: D105
        pass
