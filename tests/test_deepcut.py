import numpy as np

from deepcut import find_profiles, get_example_data


def test_get_example_data() -> None:
    data = get_example_data()
    assert data is not None
    assert isinstance(data, np.ndarray)


def test_find_profiles() -> None:
    # Load the pressure data

    pressure = get_example_data()

    # Find the profiles
    profiles = find_profiles(pressure)

    # # Check that the profiles are found correctly
    # assert len(profiles) > 0
    # assert all(isinstance(profile, np.ndarray) for profile in profiles)
