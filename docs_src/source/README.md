![python_badge](https://img.shields.io/pypi/pyversions/ternary-diagram)
![license_badge](https://img.shields.io/pypi/l/ternary-diagram)
![Total_Downloads_badge](https://pepy.tech/badge/ternary-diagram)

This package makes it easier for you to draw beautiful ternary diagram <b>without</b> [pymatgen](https://pymatgen.org).

Meaningly, only need `numpy`, `pandas` and `matplotlib`.

## What you will be able to do with this package
- Create beautiful contour maps easily
- Creating a scatter plot
- Draw tie lines
- Automatically format chemical composition using subscripts
- Most of the matplotlib options are available

![/example/contour/example_contour.png](https://github.com/yu9824/ternary_diagram/blob/main/example/contour/example_contour.png?raw=true "example")

## First of all
This package works well with the [element_recognition](https://github.com/yu9824/element_recognition) package (my own package) because it has a function (`get_ratio`) that converts composition to ratio.

For example,

```python
from element_recognition import get_ratio

get_ratio(products = ['LiLa2TiO6'], materials = ['Li2O', 'La2O3', 'TiO2'])

               Li2O  La2O3  TiO2
    Li2La2TiO6   1.0   1.0   1.0
```

## How to install
```bash
pip install ternary-diagram
```

PyPI project is [here](https://pypi.org/project/ternary-diagram/).

## Usage
See [Examples](#examples) and the [documentation](https://yu9824.github.io/ternary_diagram/).

### Examples
An easy example is here.
```python
import matplotlib.pyplot as plt
from ternary_diagram import TernaryDiagram

td = TernaryDiagram(['Li2O', 'La2O3', 'TiO2'])
td.scatter(vector = [[1, 1, 1], [1, 2, 3]], z = [0, 1])
td.scatter(vector = [[2, 1, 3], [3, 2, 1]], marker = 's', c = '#022c5e', s = 30)    # You can set some options in matplotlib.pyplot.scatter like `marker`, `c` etc.
td.plot(r1 = [1, 1, 1], r2 = [1, 2, 3], color = 'black')  # You can set some options in matplotlib.pyplot.plot like `lw`, `c`, and so on.
plt.savefig('figure.png', dpi = 144)
```

![/example/example_on_readme/figure.png](https://github.com/yu9824/ternary_diagram/blob/main/example/example_on_readme/figure.png?raw=true)

It can be written like this.
```python
import matplotlib.pyplot as plt
from ternary_diagram import TernaryDiagram

fig, ax = plt.subplots(facecolor='w')   # The background color is sometimes transparent in jupyter notebooks, so set facecolor 'white'.
td = TernaryDiagram(['Li2O', 'La2O3', 'TiO2'], ax=ax)   # You can set `ax` to select which axes to draw. If None, automatically select or generate. 
td.scatter(vector = [[1, 1, 1], [1, 2, 3]], z = [0, 1])
td.scatter(vector = [[2, 1, 3], [3, 2, 1]], marker = 's', c = '#022c5e', s = 30)    # You can set some options in matplotlib.pyplot.scatter like `marker`, `c` etc.
td.plot(r1 = [1, 1, 1], r2 = [1, 2, 3], color = 'black')  # You can set some options in matplotlib.pyplot.plot like `lw`, `c`, and so on.
fig.savefig('figure.png', dpi = 144)
```

It means that you can draw multiple figures in one figure object.


See also the [example](https://github.com/yu9824/ternary_diagram/tree/main/example) folder. In particular, if you want to know how to use element_recognition[element_recognition](https://github.com/yu9824/element_recognition) as well, please refer to [example/scatter/example _scatter_with_annotations.ipynb](https://github.com/yu9824/ternary_diagram/tree/main/example/scatter/example_scatter_with_annotations.ipynb).

### LICENSE
See [LICENSE](https://github.com/yu9824/ternary_diagram/tree/main/LICENSE).