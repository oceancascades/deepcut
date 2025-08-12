from pathlib import Path

import numpy as np
from numpy.typing import ArrayLike

from .deepcut import find_profiles

__all__ = ["find_profiles", "get_example_data"]


def get_example_data() -> ArrayLike:
    """
    Load example pressure data from the tests/data directory.
    Returns:
        ArrayLike: 1D array of pressure values.
    """
    csv_path = str(
        Path(__file__).parent.parent.parent / "tests" / "data" / "rbr_pressure.csv"
    )
    pressure = np.loadtxt(csv_path, delimiter=",", skiprows=2)
    return pressure
