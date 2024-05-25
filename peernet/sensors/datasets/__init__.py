"""Implementation of the datasets submodule.

Datasets are a special case of sensors, since they can be sampled and return
something. We implement one such dataset, of a single fixed image.
"""

__version__ = "0.0.1"
from .FixedImage import FixedImage  # noqa: F401
