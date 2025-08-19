---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# deepcut

`deepcut` is a collection of algorithms for finding profiles in ocean pressure data. 

# Usage

```{code-cell}
:tags: [hide-cell]
# Ignore this (it is helpful for the local docs build.)
import deepcut
import importlib
importlib.reload(deepcut)
```

Currently the package contains just one algorithm for identifying profiles, called `find_profiles`, which you can import it from the main package. 

```{code-cell}
from deepcut import get_example_data, find_profiles
```

The function operates on pressure time series data with no explicit need for time information (it assumes uniformly spaced data) e.g.

```{code-cell}
pressure = get_example_data()
print(pressure[:10])
```

It will identify profile segments in the data. Each segement is defined by a start index, peak index, and end index, `(start, peak, end)`.

```{code-cell}
segments = find_profiles(pressure)
print(segments)
```

The default parameters may need to be changed to find the profiles properly. Note that some smaller profiles are not identified in the following example.

```{code-cell}
import plotly.graph_objects as go
import numpy as np
from IPython.display import HTML

segments = np.asarray(segments)
start = segments[:, 0]
peak = segments[:, 1]
end = segments[:, 2]
x = np.arange(0, pressure.size)
cut = slice(0, None, 32)  # reduce data for plotting

fig = go.Figure()
fig.add_trace(go.Scatter(x=x[cut], y=pressure[cut], mode="lines", name="pressure"))
fig.add_trace(go.Scatter(x=x[start], y=pressure[start], mode="markers", name="start", marker_color="green"))
fig.add_trace(go.Scatter(x=x[peak], y=pressure[peak], mode="markers", name="peak", marker_color="blue"))
fig.add_trace(go.Scatter(x=x[end], y=pressure[end], mode="markers", name="end", marker_color="red"))
fig.update_layout(yaxis_title="Pressure (dbar)", xaxis_title="Data index (-)", yaxis_autorange="reversed")
HTML(fig.to_html(include_plotlyjs='cdn'))
```

`find_profiles` accepts a number of arguments for fine-tuning profile identification. Underneath the hood it is applying `scipy` functions [`find_peaks`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) and [`savgol_filter`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html). Consequently, most of the arguments to `find_profiles` alter the behaviour of these functions and it is helpful to be familiar with their operation. 

The profile finding algorithm roughly follows the steps below. The action of each step is modified by a set of arguments. 

| Step    | Arguments modifying the step |
| -------- | ------- |
| 1. Data are smoothed to remove noise | `window_length`, `polyorder` |
| 2. Pressure maxima are identified | `peaks_kwargs` |
| 3. Pressure minima are identified, equivalent to searching for maxima in negative pressure | `troughs_kwargs` |
| 4. Segments are cleaned up to get better estimates of where the profiles start and end | `run_length`, `min_increase`, `min_decrease` | 

The results from the example above can be improved by modifying the peak finding steps. We identify by eye that some smaller peaks are missed, suggesting that we should decrease the minimum height and prominance thresholds when finding peaks and troughs. 

```{code-cell}
peaks_kwargs = {"height": 15, "distance": 200, "width": 200, "prominence": 15}

segments = find_profiles(pressure, peaks_kwargs=peaks_kwargs)
segments = np.asarray(segments)
start = segments[:, 0]
peak = segments[:, 1]
end = segments[:, 2]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x[cut], y=pressure[cut], mode="lines", name="pressure"))
fig.add_trace(go.Scatter(x=x[start], y=pressure[start], mode="markers", name="start", marker_color="green"))
fig.add_trace(go.Scatter(x=x[peak], y=pressure[peak], mode="markers", name="peak", marker_color="blue"))
fig.add_trace(go.Scatter(x=x[end], y=pressure[end], mode="markers", name="end", marker_color="red"))
fig.update_layout(yaxis_title="Pressure (dbar)", xaxis_title="Data index (-)", yaxis_autorange="reversed")
HTML(fig.to_html(include_plotlyjs='cdn'))
```

# Glider example

Gliders return decimated (low resolution) real-time pressure data and may undertake complex dive plans. The example
below illustrates how to extract profiles in this case. Smoothing is probably unnecessary. 

```{code-cell}
from deepcut import synthetic_glider_pressure

pressure = synthetic_glider_pressure()
peaks_kwargs = {"height": 100, "distance": 5, "width": 5, "prominence": 100}
segments = find_profiles(pressure, peaks_kwargs=peaks_kwargs, smoothing=False)
segments = np.asarray(segments)
start = segments[:, 0]
peak = segments[:, 1]
end = segments[:, 2]
x = np.arange(0, pressure.size)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=pressure, mode="markers", name="pressure"))
fig.add_trace(go.Scatter(x=x[start], y=pressure[start], mode="markers", name="start", marker_color="green"))
fig.add_trace(go.Scatter(x=x[peak], y=pressure[peak], mode="markers", name="peak", marker_color="blue"))
fig.add_trace(go.Scatter(x=x[end], y=pressure[end], mode="markers", name="end", marker_color="red"))
fig.update_layout(yaxis_title="Pressure (dbar)", xaxis_title="Data index (-)", yaxis_autorange="reversed")
HTML(fig.to_html(include_plotlyjs='cdn'))
```