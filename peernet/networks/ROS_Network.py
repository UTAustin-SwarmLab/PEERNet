"""Implementation of a PEERNet compatible network built on ROS.

The ROS implementation is limited in some ways. For example, we support only
spwaning one publisher/subscriber node per device. We recommend extending
these functionalities here to support custom ROS use cases.
"""

from peernet.networks import BaseNetwork
from peernet.utils.custom_formatter import ch
import logging

import rospy  # type: ignore
from std_msgs.msg import String  # type: ignore

import socket  # only used for making sure hostnames resolve
import os

from typing import Callable


class ROS_Network(BaseNetwork):
    """Implementation of a network module that uses ROS (1) for message passing."""

    def __init__(
        self, device_name: str, master: str, verbose: int = 0, *args, **kwargs
    ):
        """Constructor."""
        # logger setup
        self.logger = logging.getLogger("ZMQ_Pair")
        if verbose == 0:
            self.logger.setLevel(logging.DEBUG)
        elif verbose == 1:
            self.logger.setLevel(logging.WARN)
        else:
            self.logger.setLevel(logging.CRITICAL)
        self.logger.addHandler(ch)

        # Call constructor for BaseNetwork
        super().__init__(verbose=verbose, **kwargs)

        # TODO: If this device is the master, spawn a process for roscore-- ignore this for now.  # noqa: E501
        if device_name == master:
            self.logger.info(
                "This device is the master. Forking process for roscore not yet implemented."  # noqa: E501
            )

        # Set required environment variables
        # Check to make sure master and self exist in /etc/hosts
        try:
            socket.gethostbyname(device_name)
        except socket.gaierror:
            self.logger.critical(f"Name {device_name} does not resolve.")

        try:
            socket.gethostbyname(master)
        except socket.gaierror:
            self.logger.critical(f"Name {master} does not resolve.")
        self.logger.debug("Hostnames resolved.")

        # Export 2 required environment variables: ROS_MASTER_URI, ROS_HOSTNAME
        os.environ["ROS_MASTER_URI"] = f"http://{master}:11311/"
        os.environ["ROS_HOSTNAME"] = f"{device_name}"

        # Instantiate one node for this process, with name = device name.
        node_name = self._get_node_name(device_name)
        rospy.init_node(node_name, anonymous=False)
        self.logger.debug(f"Initialized node named {node_name}")

        # Instantiate a single publisher -- we're not implementing multiple publishers yet.  # noqa: E501
        self.publisher = rospy.Publisher(
            self._get_topic_name(device_name), String, queue_size=10
        )
        self.logger.debug("Initialized single publisher")

    def send(self, data: str) -> None:
        """Publishes data on self.publsher.

        Args:
            data: str - Data to send. Currently only supports string.
        """
        self.publisher.publish(data)

    def register_callback(self, device: str, callback_func: Callable) -> None:
        """Registers a callback function for messages heard on {device}'s topic name.

        Args:
            device: str - Which device to register a callback for
            callback_func: Callable - A function to register as the callback
        """
        self.logger.debug(f"Attempting to register callback for device {device}")
        rospy.Subscriber(self._get_topic_name(device), String, callback_func)

    def is_shutdown(self) -> bool:
        """Just a wrapper around rospy.is_shutdown.

        This is intended so that the user does not have to directly
        interact with rospy.
        """
        return rospy.is_shutdown()

    def _get_node_name(self, device_name: str) -> str:
        """Returns the node name associated with device_name.

        This really only matters becasue we can't have '-' characters in ros topic
        names, but do allow them in DDNS names.
        """
        return device_name.replace("-", "_")

    def _get_topic_name(self, device_name: str) -> str:
        """Returns the topic name that device_name is sending messages on."""
        return self._get_node_name(device_name) + "_out"
