"""Subpackage containing metrics implementations."""
__version__ = "0.0.1"

from peernet.utils.custom_formatter import ch
import logging
logger = logging.getLogger("NETWORKS")
logger.setLevel(logging.WARNING)
logger.addHandler(ch)

from .Messages import Message  # noqa: E402, F401

#Networks submodule is old, and should not be used. Some legacy code 
#Might have it as a dependency
#from .Networks import PyZMQ_Network  # noqa: E402, F401
from .BaseNetwork import BaseNetwork  # noqa: E402, F401
from .ZMQ_Pair import ZMQ_Pair  # noqa: E402, F401
from .ZMQ_UDP import ZMQ_UDP  # noqa: E402, F401

try:
    from .ROS_Network import ROS_Network  # noqa: E402, F401
except ImportError:
    logger.warn("""Rospy might not be installed. 
                You won't be able to use ROS network functionality.""")