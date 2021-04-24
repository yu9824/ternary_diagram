# Ternary Diagram
This package makes it easier for you to draw beautiful ternary diagram <b>without</b> [pymatgen](https://pymatgen.org).

Meaningly, only need `numpy`, `pandas` and `matplotlib`.

![example](https://github.com/yu-9824/ternary_diagram/blob/main/example/contour/example_contour.png "example")

## First of all
This package works well with the [element_recognition](https://github.com/yu-9824/element_recognition) package (my own package). This package works well with the element_recognition package (my own package) because it has a function (`get_ratio`) that converts composition to ratio.

Also, if you are using Mac OS, you can use these functions in a GUI application. See [ternary_diagram_gui](https://github.com/yu-9824/ternary_diagram_gui) for details.


## How to install
I recommend you to create and use a brand new virtual environment, especially anaconda.

* pip
~~~
pip install git+https://github.com/yu-9824/ternary_diagram.git
~~~
* anaconda
~~~
conda install pip
pip install git+https://github.com/yu-9824/ternary_diagram.git
~~~

## Usage (文法)
### import package
~~~python
from ternary_diagram import TernaryDiagram
~~~

### Make an instance
~~~python
materials = ['Li2O', 'La2O3', 'TiO2']
td = TernaryDiagram(materials)
~~~
* `materials`:
    * `List` of compounds at the endpoints of the triangle, 1D, length 3. 
    * 三角図の端点となる化合物，1次元，長さ3の`list`．

### Scatter points
化合物の点をプロット．
```python
vector = [[1, 1, 1]]
td.scatter(vector, **options)
```
* `vector`:
    * percentage of each compound mixed in 2D `list` / `pandas.DataFrame` / `numpy.ndarray`, where shape = [n, 3] (n is the number of samples to be plotted as integer)
    * それぞれの化合物が混ざった割合．2次元`list` / `pandas.DataFrame` / `numpy.ndarray`で，shape = [n, 3] (nは整数でプロットしたいサンプル数)
    
* `options`:
    * most of the options available in `matplotlib.pyplot.scatter` (`color`, `marker`, etc.)
    * If you add `z` to `options`, you can change the color of the point to a gradient for each value. (It is possible to plot properties such as thermal conductivity and resistance of a material of that composition.)
    * `matplotlib.pyplot.scatter`で使えるoptionは大体使える (`color`, `marker`, ...etc.)
    * もし`z`を`options`に加えると点の色を値ごとにグラデーションにすることができる．(その組成の材料の熱伝導率や抵抗値などの特性をプロットすることができる．)

### Contour
等高線を使ったカラーマップを出力
```python
td.contour(vector, z = [...], maximum = None, minimum = None)
```
* `vector`:
    * As with `scatter`, the ratio of each compound mixed together
    * `scatter`と同様でそれぞれの化合物が混ざった割合
* `z`:
    * It should have the same length as len(vector) and is required to color the colormap.
    * len(vector)と同じ長さを持つ．colormapの色をつけるにあたって必要な値．
* `maximum`:
    * No need. If there is not, it will get the maximum value by itself.
    * なくてもいい．なかったら勝手に最大値を取得してやってくれる．
* `minimum`:
    * No need. If there is not, it will get the minimum value by itself.
    * なくてもいい．なかったら勝手に最小値を取得してやってくれる．

### Tie line (連結線)
It is possible to draw a tie line. (連結線を引くことができる．)
```python
td.plot(r1, r2, **options)
```
* `r1` and `r2`:
    * 1D, `list` of length 3. Mixing ratio of compounds at the endpoints of the connecting lines.
    * 一次元，長さ3の`list`．連結線の端点の化合物の混合割合．
* `options`:
    * `matplotlib.pyplot.plot`の`options`と同じ．(e.g. lw, color etc.)

### example
* See also the [example](https://github.com/yu-9824/ternary_diagram/tree/main/example) folder. 
* In particular, if you want to know how to use element_recognition[element_recognition](https://github.com/yu-9824/element_recognition) as well, please refer to [example/scatter/example _scatter_with_annotations.ipynb](https://github.com/yu-9824/ternary_diagram/tree/main/example/scatter/example_scatter_with_annotations.ipynb).


* [example](example)フォルダも参照．
* 特にelement_recognition[element_recognition](https://github.com/yu-9824/element_recognition)の使い方も含めて知りたい場合は[example/scatter/example_scatter_with_annotations.ipynb](https://github.com/yu-9824/ternary_diagram/tree/main/example/scatter/example_scatter_with_annotations.ipynb)を参照．
```python
td = TernaryDiagram(['Li2O', 'La2O3', 'TiO2'])
td.scatter([[1, 1, 1], [1, 2, 3]], z = [0, 1], marker = 'o')
td.plot([1, 1, 1], [1, 2, 3], color = 'black')
td.fig.savefig('figure.png', transparent = True, dpi = 300)
```

### LICENSE
See [LICENSE](https://github.com/yu-9824/ternary_diagram/tree/main/LICENSE).