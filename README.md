# Ternary Diagram

[![python_badge](https://img.shields.io/pypi/pyversions/ternary-diagram)](https://pypi.org/project/ternary-diagram/)
[![license_badge](https://img.shields.io/pypi/l/ternary-diagram)](https://pypi.org/project/ternary-diagram/)
[![PyPI version](https://badge.fury.io/py/ternary-diagram.svg)](https://pypi.org/project/ternary-diagram/)
[![Downloads](https://static.pepy.tech/badge/ternary-diagram)](https://pepy.tech/project/ternary-diagram)

[![CI](https://github.com/yu9824/ternary_diagram/actions/workflows/CI.yaml/badge.svg)](https://github.com/yu9824/ternary_diagram/actions/workflows/CI.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![conda_badge](https://anaconda.org/conda-forge/ternary-diagram/badges/version.svg)](https://anaconda.org/conda-forge/ternary-diagram/)
[![arch_badge](https://anaconda.org/conda-forge/ternary-diagram/badges/platforms.svg)](https://anaconda.org/conda-forge/ternary-diagram)

This package makes it easier for you to draw beautiful ternary diagram **without** [pymatgen](https://pymatgen.org).

Meaningly, only need `numpy` and `matplotlib`.

## What you will be able to do with this package

- Create beautiful contour maps easily
- Creating a scatter plot
- Draw tie lines
- Automatically format chemical composition using subscripts
- Most of the matplotlib options are available

![/example/contour/example_contour.png](https://github.com/yu9824/ternary_diagram/blob/main/example/contour/example_contour.png?raw=true "example")

## How to install

### PyPI

```bash
pip install ternary-diagram
```

PyPI project is [here](https://pypi.org/project/ternary-diagram/).

### Anaconda

```bash
conda install -c conda-forge ternary-diagram
```

Anaconda (conda-forge) package site is [here](https://anaconda.org/conda-forge/ternary-diagram).

## Usage

See [Examples](#examples) and the [documentation](https://yu9824.github.io/ternary_diagram/).

### Examples

An easy example is here.

```python
import matplotlib.pyplot as plt
from ternary_diagram import TernaryDiagram

# You can set `ax` to select which axes to draw. If not, the current axes will be used.
td = TernaryDiagram(["Li2O", "La2O3", "TiO2"])

# scatter
td.scatter(vector=[[1, 1, 1], [1, 2, 3]], z=[0, 1])
# You can set some options in `plt.scatter` like `marker`, `c` etc.
td.scatter(vector=[[2, 1, 3], [3, 2, 1]], marker="s", c="#022c5e", s=30)

# line plot
# You can set some options in `plt.plot` like `lw`, `c`, and so on.
td.plot([[1, 1, 1], [1, 2, 3]], color="black")

# save figure
td.fig.savefig("figure.png", dpi=144)

```

![/example/example_on_readme/figure.png](https://github.com/yu9824/ternary_diagram/blob/main/example/example_on_readme/figure.png?raw=true)

It can be written like this.
```python
# The background color is sometimes transparent in jupyter notebooks, so set facecolor 'white'.
fig, ax = plt.subplots(facecolor="w")

# You can set `ax` to select which axes to draw. If not, the current axes will be used.
td = TernaryDiagram(["Li2O", "La2O3", "TiO2"], ax=ax)

# scatter
td.scatter(vector=[[1, 1, 1], [1, 2, 3]], z=[0, 1])
# You can set some options in `plt.scatter` like `marker`, `c` etc.
td.scatter(vector=[[2, 1, 3], [3, 2, 1]], marker="s", c="#022c5e", s=30)

# line plot
# You can set some options in `plt.plot` like `lw`, `c`, and so on.
td.plot([[1, 1, 1], [1, 2, 3]], color="black")

# save figure
fig.savefig("figure.png", dpi=144)

```

It means that you can draw multiple figures in one figure object.

See also the [example](https://github.com/yu9824/ternary_diagram/tree/main/example) folder.

## Histories

### v3.1.0

- Delete `.utils._BasePlotter.get_x_y` (we should access directly).
- Resolve #10 (Create `fill` argument in `TernaryDiagram.contour`).
- Resolve #11 (Create `auto_latex_notation` argument in `TernaryDiagram`).
- Update documentation.
- Update docstrings and typings.


## LICENSE

See [LICENSE](https://github.com/yu9824/ternary_diagram/tree/main/LICENSE).

MIT Licence

Copyright (c) 2021 yu9824
