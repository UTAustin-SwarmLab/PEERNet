"""Contains a sensor that returns a random string of given length.

This type of sensor is useful for introspective tests that examine the
latency of networks with respect to payload size. Payload size should only
be measured using sys.getsizeof(pickle.dumps(string)), not the input to
sample().
"""

import numpy as np


class RandomString:
    """A valid sensor class that returns a random string of given length."""

    def __init__(self) -> None:  # noqa: D107
        pass

    def sample(self, size: int) -> str:
        """Returns a random string of length size.

        Args:
            size: int - Size of output string

        Returns:
            None
        """
        # Generate random integers
        random_bytes = np.random.randint(32, 127, size=size)

        # Convert integers to characters
        random_chars = [chr(byte) for byte in random_bytes]
        return "".join(random_chars)
