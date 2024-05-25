"""Abstract dataclass for messages.

This message type is used in many locations throughput PPERNet. For example,
inference engines expect messages as arguments. This class is a useful
abstraction that enables easy implementation of our one-way network delay
estimation scheme.
"""
from dataclasses import dataclass

from peernet.metrics import MetricLogger
from typing import Any

# Logging setup
import logging
from peernet.utils import ch

logger = logging.getLogger("cv_bench_server")
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


@dataclass
class Message:
    """Wwrapper around a python object that tacks on a metric logger for transmission.

    This is best used for pyzmq message passing. Defining these types for ROS
    requires some attention.
    """

    data: Any
    logger: MetricLogger
