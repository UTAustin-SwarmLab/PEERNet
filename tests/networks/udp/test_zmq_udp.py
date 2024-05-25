"""Tests for ZMQ UDP.

Tests in this file will not pass if simply run with pytest.
The config file test_config.yaml needs to be updated, and the appropriate
programs need to be run on the appropriate devices.
"""

from peernet.networks import ZMQ_UDP
import omegaconf
import zmq

config = omegaconf.OmegaConf.load("udp_config.yaml")


def test_local_1():
    """Tests local behavior."""
    zmq_udp = ZMQ_UDP("hostname1", **config)

    for _ in range(10):
        zmq_udp.send("hostname1", "This is a message")
        msg = zmq_udp.recv("hostname1")
        print(f"I heard {msg}")


def test_local_2():
    """Tests local behavior."""
    zmq_udp = ZMQ_UDP("hostname2", **config)

    for _ in range(10):
        zmq_udp.send("hostname2", "This is a message")
        msg = zmq_udp.recv("hostname2")
        print(f"I heard {msg}")


def test_client():
    """Tests client behavior."""
    zmq_udp = ZMQ_UDP("hostname1", **config)

    for _ in range(10):
        # send, recv each time
        zmq_udp.send("hostname2", "Message from Hostname1")

        try:
            msg = zmq_udp.recv("hostname2")
            print(f"Heard {msg} from hostname2")
        except zmq.error.Again:
            print("Missed a message!")


def test_server():
    """Tests server behavior."""
    zmq_udp = ZMQ_UDP("hostname2", **config)

    for _ in range(10):
        # recv, send each time
        try:
            msg = zmq_udp.recv("hostname1")
            print(f"Heard {msg} from hostname1")
        except zmq.error.Again:
            print("Missed a message!")

        zmq_udp.send("hostname1", "Message from hostname2")
