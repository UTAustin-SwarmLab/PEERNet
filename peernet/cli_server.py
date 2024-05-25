"""Server side implementation of offloaded inference CLI."""
from peernet.inference import get_engine

import omegaconf

# Logging setup
import logging
from peernet.utils import ch

logger = logging.getLogger("cv_bench_server")
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


def server_main(
    device_name: str,
    net_type: str,
    net_config_file: str,
    num_iterations: int,
    model_name: str,
    device: str,
):
    """Main method for cli server."""
    # Cases on network type
    net_config = omegaconf.OmegaConf.load(net_config_file)
    if net_type == "zmq-tcp":
        logger.debug("Setting up zmq tcp network")
        from peernet.networks import ZMQ_Pair

        network = ZMQ_Pair(device_name=device_name, **net_config)

    elif net_type == "zmq-udp":
        logger.debug("Setting up zmq udp network")
        logger.error("This isn't implemented yet!")

    elif net_type == "ros":
        logger.debug("Setting up ros network")
        logger.error("This isn't implemented yet!")

    else:
        logger.error("Something went wrong.")

    # returns a new class with a callback method that wraps a call to DummyModel
    # infer with timing and message passing. ie is an instance of that "engine
    ie = get_engine(model_name, device)

    # Setup the network to poll, calling back to whichever inference engine is used.
    network.poll(num_iterations, ie.callback)
