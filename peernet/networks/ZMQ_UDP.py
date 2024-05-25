"""Implements a PEERNet compatible network through ZQM using UDP."""

from peernet.networks import BaseNetwork
from peernet.utils.custom_formatter import ch
import logging
import getpass
import zmq


class ZMQ_UDP(BaseNetwork):
    """Subclass of BaseNetwork that implements message passing with ZMQ Radio Dish.

    Radio Dish is currently the only ZMQ messaging pattern that supports UDP.
    """

    def __init__(
        self,
        device_name: str,
        start_port: int = 5551,
        verbose: int = 0,
        *args,
        **kwargs,
    ):
        """Constructor.

        Args:
            device_name:str - Name to assign this device.
            start_port:int - Port to start assigning ports from.
            verbose:int - 0/1/2 scale for logging verbosity.
            *args :- To pass to BaseNetwork
            **kwargs :- To pass to Base Network.
        """
        super().__init__(verbose=verbose, **kwargs)

        # logger setup
        self.logger = logging.getLogger("ZMQ_UDP")
        if verbose == 0:
            self.logger.setLevel(logging.DEBUG)
        elif verbose == 1:
            self.logger.setLevel(logging.WARN)
        else:
            self.logger.setLevel(logging.CRITICAL)
        self.logger.addHandler(ch)

        # Who am I?
        if device_name in self.device_number:
            self.name = device_name
        else:
            self.logger.warning("Invalid device_name, defaulting to getuser()")
            self.name = getpass.getuser()
        self.number = self.device_number[self.name]

        # set the range of ports that we're going to use, 2d list
        self.ports = [
            [start_port + j for i in range(self.NUM_DEVICES)]
            for j in range(self.NUM_DEVICES)
        ]
        self.logger.debug(f"Using port dictionary: {self.ports}")

        # Create lists for the 2 * N sockets we need on this device.
        self.send_sockets = [None] * self.NUM_DEVICES
        self.recv_sockets = [None] * self.NUM_DEVICES

        # Create one more list to keep track of what group numbers I assign
        # self.groups = [None]*self.NUM_DEVICES

        # Reverse mapping used to find out what name sent me a message when a particular
        # socket I poll has a new message
        self.recv_socket_mapping = dict()

        context = zmq.Context()

        # For the udp implementation, let's setup the receiving sockets, of type
        # DISH, first, and bind these to ports on our device.
        for send_device in self.device_number:
            send_device_number = self.device_number[send_device]
            dish = context.socket(zmq.DISH)

            port = self.ports[send_device_number][self.number]

            # udp stuff
            dish.rcvtimeo = 1_000  # Corresponds to 1 second, don't know what this does
            dish.bind(f"udp://*:{port}")
            group = "1"  # str(send_device_number)
            dish.join(group)

            self.recv_sockets[send_device_number] = dish
            self.recv_socket_mapping[dish] = send_device
            # self.groups[send_device_number] = group

            self.logger.debug(
                f"Established DISH socket to receive from {send_device}, device number: {send_device_number}, port: {port}, group: {group}"  # noqa: E501
            )

        # Setting up the transmitting sockets, all connected to the end device
        # These are of type zmq.RADIO
        for recv_device in self.device_number:
            recv_device_number = self.device_number[recv_device]
            recv_dns_name = self.get_ip(recv_device)

            # udp stuff
            radio = context.socket(zmq.RADIO)
            port = self.ports[self.number][recv_device_number]
            radio.connect(f"udp://{recv_dns_name}:{port}")

            self.send_sockets[recv_device_number] = radio

            self.logger.debug(
                f"Established RADIO socket to send to {recv_device}, device_number: {recv_device_number}, port: {port}"  # noqa: E501
            )

        # TODO: Set up polling here

    def send(self, destination: str, data):
        """Send (data) to destination.

        destination - a hostname, not an IP or dns name
        """
        # lookup the right socket to use
        dest_number = self.device_number[destination]
        radio = self.send_sockets[dest_number]
        # group = self.groups[dest_number]

        # Send using default pickle serialization
        radio.send_pyobj(data, group="1")

    def recv(self, source: str):
        """Block for a maximum of rcvtimeo while waiting to receive data from source.
        
        If you would like to change rcvtimeo, edit the constructor.
        """
        source_device_number = self.device_number[source]
        dish = self.recv_sockets[source_device_number]

        return dish.recv_pyobj()

    def close(self):
        """Close all the sockets."""
        for socket in self.send_sockets:
            socket.close()

        for socket in self.recv_sockets:
            socket.close()
