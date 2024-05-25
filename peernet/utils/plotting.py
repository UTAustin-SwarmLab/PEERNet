"""General plotting utils used in CLI."""

import pathlib

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot_histogram(
    data: pd.Series, title: str, xlabel: str, ylabel: str, out: pathlib.Path
):
    """Plots a histogram of data to out."""
    plt.figure()

    # Plotting the histogram
    sns.histplot(data)

    # Adding labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # Display the plot
    plt.savefig(out)


def generate_plots(result_dir: pathlib.Path, drop_rows=True):
    """Generates latency and throughput density plots."""
    # Read data into csv
    df = pd.read_csv(result_dir / "data.csv")
    if drop_rows:
        df = df.iloc[5:]

    # Make histogram of each individual time
    plot_histogram(
        df["inference"],
        "Inference Time",
        "Time (sec)",
        "Frequency",
        result_dir / "inference-time.png",
    )
    plot_histogram(
        df["download"],
        "Download Time",
        "Time (sec)",
        "Frequency",
        result_dir / "download-time.png",
    )
    plot_histogram(
        df["upload"],
        "Upload Time",
        "Time (sec)",
        "Frequency",
        result_dir / "upload-time.png",
    )
    plot_histogram(
        df["upload-throughput"],
        "Upload Throughput",
        "Throughput (bps)",
        "Frequency",
        result_dir / "upload-throughput.png",
    )
    plot_histogram(
        df["download-throughput"],
        "Download Throughput",
        "Throughput (bps)",  # noqa: E501
        "Frequency",
        result_dir / "download-throughput.png",
    )
    plot_histogram(
        df["sensing"],
        "Sensing Time",
        "Time (sec)",
        "Frequency",
        result_dir / "sensing-time.png",
    )
