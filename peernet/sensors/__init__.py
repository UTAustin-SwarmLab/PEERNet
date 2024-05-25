"""The sensors submodule is responsible for abstracting input to devices.

Sensors are anything that can be "sampled" from. The only requirement for an
object to be a sensor is for it to contain a sample() method. Datasets are a
specific type of sensors, and we implement one dataset-- a fixed image that
returns the same image over and over again on calls to sample(). We implement
one dummy test sensor, RandomString, that returns a random string of requested
length.

Additionally, we implement get_sensor, a method for sensor selection, which allows
users to pass in a string pointing to a sensor class in another file. get_sensor()
will execute a runtime import and return the requested object as a sensor.
"""

__version__ = "0.0.1"
from .Protocols import Sensor  # noqa: F401
from .get_sensor import get_sensor  # noqa: F401
from .random_string import RandomString  # noqa: F401
