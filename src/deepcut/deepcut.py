from typing import Any

import numpy as np
from numpy.typing import ArrayLike
from scipy.signal import find_peaks, savgol_filter

_default_peaks_kwargs = {"height": 25, "distance": 500, "width": 500, "prominence": 25}


def find_profiles(
    pressure: ArrayLike,
    window_length: int = 32,
    polyorder: int = 2,
    smoothing: bool = True,
    run_length: int = 10,
    min_increase: float = 0.01,
    min_decrease: float = -0.01,
    peaks_kwargs: dict[str, Any] | None = None,
    troughs_kwargs: dict[str, Any] | None = None,
) -> list[tuple[int, int, int]]:
    """
    Find profile segments in a pressure time series from a profiling instrument.

    Parameters
    ----------
    pressure : array_like
        1D array of pressure values sampled continuously.
    window_length : int, optional
        Window length for Savitzky-Golay smoothing filter (default: 32).
    polyorder : int, optional
        Polynomial order for Savitzky-Golay filter (default: 2).
    smoothing : bool, optional
        If True (default), apply Savitzky-Golay smoothing to the pressure data before analysis.
        If False, use the raw pressure data.
    run_length : int, optional
        Number of consecutive samples required to confirm descent/ascent (default: 10).
    min_increase : float, optional
        Minimum pressure increase per sample to confirm descent (default: 0.01).
    min_decrease : float, optional
        Maximum pressure decrease per sample to confirm ascent (default: -0.01).
    peaks_kwargs : dict, optional
        Dictionary of keyword arguments to pass to scipy.signal.find_peaks for peak detection.
    troughs_kwargs : dict, optional
        If not specified, the peaks_kwargs will be used.

    Returns
    -------
    segments : list of tuple
        List of (start, peak, end) index tuples for each detected profile segment.
        Each segment starts at the first robust descent after a surface trough,
        peaks at the profile maximum, and ends at the last robust ascent before the next surface trough.

    Notes
    -----
    - The function can use Savitzky-Golay smoothing to reduce noise if smoothing=True.
    - Profile start and end indices are refined to avoid long periods near the surface.
    - Troughs are detected as local minima in the (optionally smoothed) pressure signal.
    - Additional arguments for peak/trough detection can be passed via peaks_kwargs and troughs_kwargs.
    """
    pressure = np.asarray(pressure)

    if not np.isfinite(pressure).all():
        raise ValueError("Input pressure data contains non-finite values.")

    if smoothing:
        pressure_smooth = savgol_filter(
            pressure, window_length=window_length, polyorder=polyorder
        )
    else:
        pressure_smooth = pressure
    ndata = pressure.size
    diffs = np.diff(pressure_smooth)

    if peaks_kwargs is None:
        peaks_kwargs = _default_peaks_kwargs
    if troughs_kwargs is None:
        troughs_kwargs = peaks_kwargs

    peaks, _ = find_peaks(pressure_smooth, **peaks_kwargs)
    troughs, _ = find_peaks(pressure_smooth.max() - pressure_smooth, **troughs_kwargs)

    segments = []
    for peak in peaks:
        # Find surface point before peak
        trough_before = troughs[troughs < peak]
        start = trough_before[-1] if len(trough_before) > 0 else 0

        # Move start forward to first robust descent
        for i in range(start, peak - run_length):
            if np.all(diffs[i : i + run_length] > min_increase):
                start = i
                break

        # Find surface point after peak
        trough_after = troughs[troughs > peak]
        end = trough_after[0] if len(trough_after) > 0 else ndata - 1

        # Move end backward to last robust ascent
        for i in range(end, peak + run_length, -1):
            if i - run_length >= peak and np.all(
                diffs[i - run_length : i] < min_decrease
            ):
                end = i
                break

        segments.append((int(start), int(peak), int(end)))
    return segments
