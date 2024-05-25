"""Tests for the base network.

Tests in this file will not pass if simply run with pytest.
The config file test_config.yaml needs to be updated, and the appropriate
programs need to be run on the appropriate devices.
"""
from peernet.networks import BaseNetwork
import omegaconf

config = omegaconf.OmegaConf.load("test_config.yaml")

def test_base_construction():
    """Tests construction of a base network."""
    try:
        _ = BaseNetwork(**config)
        assert True

    except:  # noqa: E722
        assert False

def test_ip_lookup():
    """Tests the ip lookup function."""
    basenet = BaseNetwork(verbose=2, **config)
    assert basenet.get_ip("hostame1") == config.devices["hostame1"]
    assert basenet.get_ip("hostame_1") == -1

def test_hostname_lookup():
    """Tests the hostname lookup function."""
    basenet = BaseNetwork(verbose = 2, **config)
    assert basenet.get_hostname(basenet.get_ip("hostame1")) == "hostame1"
    assert basenet.get_hostname(basenet.get_ip("hostame_1")) == -1