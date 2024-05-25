"""Subpackage containing inference implementations.

The inference submodule abstracts computation on devices. This includes
traditional ML workload inference as well as non-ML processing. The module
is named inference to represent ML workloads, which we see being the most
common.
"""

__version__ = "0.0.1"

from peernet.utils.custom_formatter import ch
import logging

logger = logging.getLogger("INFERENCE")
logger.setLevel(logging.WARNING)
logger.addHandler(ch)

from .Protocols import Inference  # noqa: F401, E402
from .DummyInference import DummyModel  # noqa: F401, E402

try:
    from .TorchvisionPretrained import TorchvisionPretrainedClassifier  # noqa: F401
except ImportError:
    logger.warn("""Couldn't resolve pytorch imports. You won't be able to use the 
                TorchvisionPretrainedClassifier inference object. Make sure pytorch 
                 is available or install this package with the torch option.""")

from .enginize import enginize, get_engine  # noqa: F401, E402
