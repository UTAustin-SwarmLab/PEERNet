"""Tests for ROS Networks.

Tests in this file will not pass if simply run with pytest.
The config file test_config.yaml needs to be updated, and the appropriate
programs need to be run on the appropriate devices.
"""

from peernet.networks import ROS_Network
import omegaconf
import time

config = omegaconf.OmegaConf.load("test_config.yaml")


def test_construction():
    """Tests construction of a ROS Network."""
    _ = ROS_Network("hostname1", "hostname2", **config)


def test_send():
    """Tests publishing."""
    ros_network = ROS_Network("hostname1", "hostname2", **config)

    for _ in range(100):
        ros_network.send("Hello!")
        time.sleep(1)

        if ros_network.is_shutdown():
            assert True
            break


def test_recv():
    """Tests receiving as if it were the other device in the pipeline."""
    ros_network = ROS_Network(device_name="hostname2", master="hostname2", **config)
    ros_network.register_callback("hostname1", dummy_callback)

    while not ros_network.is_shutdown():
        pass


def dummy_callback(data):
    """Dummy callback function to be used by other tests."""
    print(f"Dummy callback heard data {data}")


def test_local_send_recv():
    """Tests local send and receive."""
    ros_network = ROS_Network("hostname1", "hostname2", **config)

    ros_network.register_callback("hostname1", dummy_callback)

    for _ in range(100):
        ros_network.send("Hello!")
        time.sleep(1)

        if ros_network.is_shutdown():
            assert True
            break
