"""Tests for ZMQ PAIR (Client side).

Tests in this file will not pass if simply run with pytest.
The config file test_config.yaml needs to be updated, and the appropriate
programs need to be run on the appropriate devices.
"""

from peernet.networks import ZMQ_Pair
import omegaconf

config = omegaconf.OmegaConf.load("test_config.yaml")


def test_instantiation():
    """Tests instantiation."""
    _ = ZMQ_Pair("hostname1", **config)


def test_simple():
    """Tests simple behavior."""
    zmq_pair = ZMQ_Pair("hostname1", **config)

    for _ in range(5):
        print(f"Received: {zmq_pair.recv('hostame2')} from hostname2")
        zmq_pair.send("hostame2", "hi from hostname1")
