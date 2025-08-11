from importlib.resources import files

import numpy as np

from deepcut import find_profiles


def test_find_profiles() -> None:
    # Load the pressure data

    csv_path = str(files("tests") / "data/rbr_pressure.csv")
    pressure = np.loadtxt(csv_path, delimiter=",", skiprows=2)

    # Find the profiles
    profiles = find_profiles(pressure)

    # # Check that the profiles are found correctly
    # assert len(profiles) > 0
    # assert all(isinstance(profile, np.ndarray) for profile in profiles)
