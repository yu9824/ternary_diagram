## how to install (インストール方法)
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
~~~
from ternary_diagram import ternary_diagram
~~~

### Make an instance
~~~
materials = ['Li2O', 'LaO3', 'TiO2']
td = ternary_diagram(materials)
~~~
* `materials`:
    * `List` of compounds at the endpoints of the triangle, 1D, length 3. 
    * 三角図の端点となる化合物，1次元，長さ3の`list`．

### Scatter points
化合物の点をプロット．
```
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
```
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
```
td.plot(r1, r2, **options)
```
* `r1` and `r2`:
    * 1D, `list` of length 3. Mixing ratio of compounds at the endpoints of the connecting lines.
    * 一次元，長さ3の`list`．連結線の端点の化合物の混合割合．
* `options`:
    * `matplotlib.pyplot.plot`の`options`と同じ．(e.g. lw, color etc.)

### example
See also the example folder. (exampleフォルダも参照．)
```
td = ternary_diagram(['Li2O', 'LaO3', 'TiO2'])
td.scatter([[1, 1, 1], [1, 2, 3]], z = [0, 1], marker = 'o')
td.plot([1, 1, 1], [1, 2, 3], color = 'black')
td.fig.savefig('figure.png', transparent = True, dpi = 300)
```
