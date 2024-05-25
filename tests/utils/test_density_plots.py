"""Tests utilities in utils/plotting.py."""

from peernet.utils import plotting
import pathlib


def test_density_plots():
    """Ensures density plots are created properly. Only validation is visual."""
    plotting.generate_plots(pathlib.Path("resources"), drop_rows=True)
