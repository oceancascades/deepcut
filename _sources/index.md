---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# deepcut

`deepcut` is a collection of algorithms for finding profiles from ocean pressure. 

# Usage


```{code-cell}
:tags: [hide-cell]
import deepcut
import importlib
importlib.reload(deepcut)
```

Currently the package contains one algorithm for identifying profiles, called `find_profiles`, which you can import it from the main package. 

```{code-cell}
from deepcut import get_example_data, find_profiles
```

The function operates on pressure time series data, e.g.

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

The sequence of events is roughly:
* Data are smoothed to remove small-scale noise. (`window_length`, `polyorder`)
* Pressure maxima are identified. (`peaks_kwargs`)
* Pressure minima are identified, equivalent to searching for maxima in negative pressure. (`troughs_kwargs`)
* The sequence of maxima and minima are cleaned up to get better estimates of where the profiles start and end. (`run_length`, `min_increase`, `min_decrease`)

```{code-cell}
peaks_kwargs = {"height": 15, "distance": 200, "width": 200, "prominence": 15}

segments = find_profiles(pressure, peaks_kwargs=peaks_kwargs, troughs_kwargs=peaks_kwargs)
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