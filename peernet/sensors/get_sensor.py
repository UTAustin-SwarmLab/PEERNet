"""Implements sensor retrieval.

Specifically, implements get_sensor(), a method that returns either:
1. An instantiated sensor from the implementations within PEERNet
2. A user object imported at runtime given a location description.
"""

from peernet.sensors.datasets import FixedImage
from peernet.sensors import Sensor
import importlib
import os
import sys

# logger setup
import logging
from peernet.utils import ch

logger = logging.getLogger("get_sensor")
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


def get_sensor(sensor_type: str, dataset_loc: str, sensor_object: str) -> Sensor:
    """Returns a valid sensor object.

    Specifically, handles runtime imports from user-generated modules, as
    well as pre-implemented sensor modules.

    Args:
        sensor_type: 'external', 'image', or 'random string'
        dataset_loc: if sensor_type == 'image', location of image
        sensor_object: if sensor_type == 'external', formatted string dictating
            location of sensor object to import

    Returns:
        A valid sensor object (i.e has a sample() method)

    Raises:
        ValueError: Invalid sensor_type
    """
    if sensor_type == "external":
        # Get the current working directory
        current_dir = os.getcwd()

        # Add the current directory to sys.path if not already included
        if current_dir not in sys.path:
            sys.path.append(current_dir)

        logger.debug(f"Attempting to import external sensor {sensor_object}")
        module_name, object_name = sensor_object.split("::")
        user_module = importlib.import_module(module_name)
        user_object = getattr(user_module, object_name)

        if not isinstance(user_object, Sensor):
            logger.error(f"""Object {user_object} from module {user_module} 
                         does not satisfy the Sensor Protocol.""")
            raise TypeError(f"""Object {user_object} from module {user_module} 
                         does not satisfy the Sensor Protocol.""")

        return user_object

    elif sensor_type == "image":
        return FixedImage(dataset_loc)

    elif sensor_type == "random string":
        from peernet.sensors import RandomString

        return RandomString()

    else:
        logger.error(f"sensor_type {sensor_type} does not exist.")
        raise ValueError(f"sensor_type {sensor_type} does not exist.")
