"""Implementation of a PEERNet compatible network through ZMQ TCP."""

from peernet.networks import BaseNetwork
from peernet.networks import Message
from peernet.metrics import Timer, Value

from peernet.utils.custom_formatter import ch
import logging
import getpass
import zmq
import sys
import pickle


class ZMQ_Pair(BaseNetwork):
    """Subclass of BaseNetwork that implements message passing using ZMQ with TCP.

    with Pair-communication (each device can directly
    address any other device).
    """

    def __init__(self, device_name, start_port=5551, verbose=0, *args, **kwargs):
        """Constructor."""
        super().__init__(verbose=verbose, **kwargs)

        # logger setup
        self.logger = logging.getLogger("ZMQ_Pair")
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

        self.ports = [
            [start_port + i for i in range(self.NUM_DEVICES)]
            for j in range(self.NUM_DEVICES)
        ]
        self.logger.debug(f"Using port dictionary: {self.ports}")

        # Create lists for the 2 * N sockets we need on this device.
        self.send_sockets = [None] * self.NUM_DEVICES
        self.recv_sockets = [None] * self.NUM_DEVICES
        self.recv_socket_mapping = dict()

        context = zmq.Context()

        # setup the sending sockets, all bound to me
        for recv_device in self.device_number:
            recv_device_number = self.device_number[recv_device]
            socket = context.socket(zmq.PAIR)
            port = self.ports[self.number][recv_device_number]

            self.logger.debug(
                f"Setting up sending socket to talk to {recv_device} on port {port}, bound to me."  # noqa: E501
            )

            socket.bind(f"tcp://*:{port}")
            self.send_sockets[recv_device_number] = socket

        # Setup the receiving sockets - all connected to ports on OTHER devices
        for send_device in self.device_number:
            send_device_number = self.device_number[send_device]
            send_dns_name = self.get_ip(send_device)
            socket = context.socket(zmq.PAIR)
            port = self.ports[send_device_number][self.number]
            socket.connect(f"tcp://{send_dns_name}:{port}")
            self.recv_sockets[send_device_number] = socket

            self.recv_socket_mapping[socket] = send_device

        # set up some objects for polling
        self.poller = zmq.Poller()
        for r_s in self.recv_sockets:
            self.poller.register(r_s, zmq.POLLIN)

    def send(self, destination: str, data):
        """Send (data) to destination.

        destination - a hostname, not an IP
        """
        # lookup the right socket to use
        dest_number = self.device_number[destination]
        socket = self.send_sockets[dest_number]

        # Send using pickle serialization
        socket.send_pyobj(data)

    def send_with_timing(self, destination: str, data, logger, section_name):
        """Sends with timing using our serialized logger format."""
        msg = Message(data, logger)

        msg.logger.log_section(section_name, Timer)

        self.send(destination, msg)

    def recv(self, source: str):
        """Block while waiting to receive data from source."""
        source_device_number = self.device_number[source]
        socket = self.recv_sockets[source_device_number]

        return socket.recv_pyobj()

    def recv_with_timing(self, source: str, logger, section_name, log_bytes=True):
        """Receives with timing using our serialized logger format."""
        recv_msg = self.recv(source)
        recv_msg.logger.end_sub(section_name)

        msg_bytes = sys.getsizeof(pickle.dumps(recv_msg))
        data_bytes = sys.getsizeof(pickle.dumps(recv_msg.data))

        recv_msg.logger.log_section(f"{section_name}-msg-bytes", Value).end_collection(
            msg_bytes
        )
        recv_msg.logger.log_section(f"{section_name}-data-bytes", Value).end_collection(
            data_bytes
        )

        logger.copy_from(recv_msg.logger)

        return recv_msg.data

    def poll(self, max_msg_count, callback=None):
        """Polls for messages on all registered recv_sockets.

        This is a blocking function. Set max_msg_count wisely.
        """
        for _ in range(max_msg_count):
            incoming_messages = dict(self.poller.poll())

            # Go through all our receiving sockets to see who set off the poll.
            for receiver in self.recv_sockets:
                if receiver in incoming_messages:
                    sending_device = self.recv_socket_mapping[receiver]

                    msg = receiver.recv_pyobj()

                    call_out = "ack"
                    if callback:
                        call_out = callback(msg)

                    # Send an ack back
                    self.logger.debug(f"Sending acknowledgement to {sending_device}")
                    self.send(sending_device, call_out)

    def close(self):
        """Close all the sockets."""
        for socket in self.send_sockets:
            socket.close()

        for socket in self.recv_sockets:
            socket.close()
