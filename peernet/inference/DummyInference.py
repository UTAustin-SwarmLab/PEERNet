"""Fake inference object to demonstrate use of inference objects."""

import time
from typing import Any


class DummyModel:
    """Fake inference object that just sleeps during processing."""

    def __init__(self, inference_time: float = 0.1) -> None:
        """Constructor.

        Args:
            inference_time: float - Total time to sleep.
        """
        self.inference_time = inference_time

    def preprocess(self, x: Any) -> Any:
        """Sleeps for 0.01 seconds and forwards to infer()."""
        time.sleep(0.01)
        return x

    def infer(self, data: Any) -> Any:
        """Sleeps for inference_time minus 0.02 seconds and forwards to postprocess."""
        time.sleep(self.inference_time - 0.02)
        return 0

    def postprocess(self, inference_output: Any) -> Any:
        """Sleeps for 0.01 seconds."""
        time.sleep(0.01)
        return inference_output
