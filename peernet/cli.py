"""Driver implementation of Benchmarking utility for offloaded inference."""

import click
import pathlib

import sys
import os

# Logging setup
from peernet.utils import ch
import logging

logger = logging.getLogger("cv_bench")
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

# Get the current working directory
current_dir = os.getcwd()

# Add the current directory to sys.path if not already included
if current_dir not in sys.path:
    sys.path.append(current_dir)


@click.command()
@click.option("--server", "device_type", flag_value="server", default=True)
@click.option("--client", "device_type", flag_value="client")
@click.option("--name", "device_name", required=True, type=str)
@click.option(
    "--network",
    "net_type",
    type=click.Choice(["zmq-tcp", "zmq-udp", "ros"], case_sensitive=False),
    help="Specify the network type.",
    required=True,
    default="zmq-tcp",
)
@click.option(
    "--network-config",
    "net_config",
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to the network configuration file.",
)
@click.option("--sensor-type", "sensor_type", type=str, default="image")
@click.option(
    "--dataset-loc",
    "dataset_loc",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Location of the dataset if using dataset sensor(image)",
)
@click.option(
    "--sensor-object",
    "sensor_object",
    type=str,
    help="location of the sensor object if passing an external sensor from your own code.",  # noqa: E501
)
@click.option("--iterations", "num_iterations", required=True, type=int)
@click.option(
    "--result-loc",
    "results",
    required=False,
    type=click.Path(
        exists=False, file_okay=False, dir_okay=True, path_type=pathlib.Path
    ),
)
@click.option("--model-name", "model_name", required=True, type=str, default="dummy")
@click.option("--device", "device", required=False, default="cuda:0", type=str)
@click.option("--generate-plots", "generate_plots", flag_value=True)
def main(
    device_type,
    device_name,
    net_type,
    net_config,
    sensor_type,
    dataset_loc,
    sensor_object,
    num_iterations,
    results,
    model_name,
    device,
    generate_plots,
):
    """Entrypoint."""
    for path in sys.path:
        logger.debug(path)

    if device_type == "server":
        logger.debug("This is a server")
        from peernet.cli_server import server_main

        server_main(
            device_name, net_type, net_config, num_iterations, model_name, device
        )

    elif device_type == "client":
        logger.debug("This is a client")

        if not dataset_loc and not sensor_object:
            logger.error(
                "Argument --dataset-loc or --sensor-object require for client device"
            )

        from peernet.cli_client import client_main

        client_main(
            device_name,
            net_type,
            net_config,
            sensor_type,
            dataset_loc,
            sensor_object,
            num_iterations,
            results,
            generate_plots,
        )

    else:
        logger.error("Must set either server or client flag")


if __name__ == "__main__":
    main()
