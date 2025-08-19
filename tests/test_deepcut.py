import numpy as np

from deepcut import find_profiles, get_example_data, synthetic_glider_pressure


def test_get_example_data() -> None:
    data = get_example_data()
    assert isinstance(data, np.ndarray)
    assert np.isfinite(data).all()


def test_synthetic_glider_pressure() -> None:
    pressure = synthetic_glider_pressure()
    assert pressure.shape == (200,)


def test_find_profiles() -> None:
    pressure = get_example_data()
    peaks_kwargs = {"height": 15, "distance": 200, "width": 200, "prominence": 15}
    segments = find_profiles(pressure, peaks_kwargs=peaks_kwargs)
    assert len(segments) == 12

    pressure = synthetic_glider_pressure(
        n_points=200, max_p=500.0, intermediate_p=200.0, n_cycles=5
    )
    peaks_kwargs = {"height": 100, "distance": 5, "width": 5, "prominence": 100}
    segments = find_profiles(pressure, peaks_kwargs=peaks_kwargs, smoothing=False)
    assert len(segments) == 6
