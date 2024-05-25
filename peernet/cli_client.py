"""Client side implementation of offloaded inference CLI."""
from peernet.sensors import get_sensor
from peernet.networks import Message
from peernet.metrics import Container, Timer, Timing, Value
from peernet.utils.plotting import generate_plots

import omegaconf
import pathlib
from tqdm import tqdm

import pickle
import sys

# Logging setup
import logging
from peernet.utils import ch

logger = logging.getLogger("cv_bench_client")
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)


def client_main(
    device_name: str,
    net_type: str,
    net_config_file: str,
    sensor_type: str,
    dataset_loc: str,
    sensor_object: str,
    num_iterations: int,
    results: pathlib.Path,
    plot: bool,
):
    """Main method for client side."""
    # Make sure the path is ok first and error out if it's not
    if results.exists():
        logger.warning(
            "Results path already exists. It's contents might be overwritten at the *end* of the run."  # noqa: E501
        )
    else:
        logger.debug(f"Creating path for {results}")
        results.mkdir(parents=True, exist_ok=True)

    # Network configuration stuffs
    net_config = omegaconf.OmegaConf.load(net_config_file)
    if net_type == "zmq-tcp":
        logger.debug("Setting up zmq tcp network")
        from peernet.networks import ZMQ_Pair

        network = ZMQ_Pair(device_name=device_name, **net_config)

    elif net_type == "zmq-udp":
        logger.debug("Setting up zmq udp network")
        from peernet.networks import ZMQ_UDP  # noqa: F401

    elif net_type == "ros":
        logger.debug("Setting up ros network")

    else:
        logger.error("Something went wrong.")

    # setup dataset
    sensor = get_sensor(sensor_type, dataset_loc, sensor_object)

    # Setup logger
    data_logger = Container(f"cv-bench-{device_name}")

    for idx in tqdm(range(num_iterations)):
        # Get a timing container for this iteration
        iter_l = data_logger.log_section(f"{idx}", Container)

        # Sample an image from the dataset
        with Timing(iter_l, "sensing"):
            sample = sensor.sample()

        # Turn the sample into a Message
        msg = Message(sample, iter_l)

        # Compute the serialized size right now, but only add it to the logger later
        up_size = sys.getsizeof(pickle.dumps(msg))
        up_logger_size = sys.getsizeof(pickle.dumps(msg.logger))

        # Send the message to the cloud-- start a sub-logger with the name 'upload'
        iter_l.log_section("upload", Timer)
        network.send(net_config.server, msg)

        # Block while waiting for a response
        recv_msg: Message = network.recv(net_config.server)

        # Copy the recv_message logger after ending the download time
        recv_msg.logger.end_sub("download")
        iter_l.copy_from(recv_msg.logger)

        # Log the received size correctly now
        down_size = sys.getsizeof(pickle.dumps(recv_msg))
        down_logger_size = sys.getsizeof(pickle.dumps(recv_msg.logger))
        iter_l.log_section("download-bytes", Value).end_collection(down_size)
        iter_l.log_section("download-logger-bytes", Value).end_collection(
            down_logger_size
        )

        # Now we can add the uploaded size correctly
        iter_l.log_section("upload-bytes", Value).end_collection(up_size)
        iter_l.log_section("upload-logger-bytes", Value).end_collection(up_logger_size)

        # Log the throughput(s), a computed value
        # Am I computing bits per second correctly? This is quite fast!
        upload_throughput = (
            8 * iter_l.get_metric("upload-bytes") / iter_l.get_metric("upload")
        )
        iter_l.log_section("upload-throughput", Value).end_collection(upload_throughput)

        download_throughput = (
            8 * iter_l.get_metric("download-bytes") / iter_l.get_metric("download")
        )
        iter_l.log_section("download-throughput", Value).end_collection(
            download_throughput
        )

        # logger.info(f"Completed iteration {idx+1}/{num_iterations}")

        if num_iterations > 1000 and (idx + 1) % 1000 == 0:
            data_logger.to_csv(results / "data.csv")

    # Write all the results
    logger.debug(data_logger)
    data_logger.to_csv(results / "data.csv")

    if plot:
        generate_plots(results)
