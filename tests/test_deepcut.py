import numpy as np

from deepcut import find_profiles, get_example_data


def test_get_example_data() -> None:
    data = get_example_data()
    assert data is not None
    assert isinstance(data, np.ndarray)


def test_find_profiles() -> None:
    pressure = get_example_data()
    peaks_kwargs = {"height": 15, "distance": 200, "width": 200, "prominence": 15}
    segments = find_profiles(pressure, peaks_kwargs=peaks_kwargs)
    assert len(segments) == 12
