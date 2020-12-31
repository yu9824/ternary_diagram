# Ternary Diagram
相図描画を簡単に行うためのパッケージ．

![example](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiIHN0YW5kYWxv%0AbmU9Im5vIj8+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBT%0AVkcgMS4xLy9FTiIKICAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZH%0ALzEuMS9EVEQvc3ZnMTEuZHRkIj4KPCEtLSBDcmVhdGVkIHdpdGggbWF0cGxv%0AdGxpYiAoaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8pIC0tPgo8c3ZnIGhlaWdo%0AdD0iMjgwLjM4NTQ2NnB0IiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCAz%0ANzAuNzE2MDE4IDI4MC4zODU0NjYiIHdpZHRoPSIzNzAuNzE2MDE4cHQiIHht%0AbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9%0AImh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiPgogPGRlZnM+CiAgPHN0%0AeWxlIHR5cGU9InRleHQvY3NzIj4KKntzdHJva2UtbGluZWNhcDpidXR0O3N0%0Acm9rZS1saW5lam9pbjpyb3VuZDt9CiAgPC9zdHlsZT4KIDwvZGVmcz4KIDxn%0AIGlkPSJmaWd1cmVfMSI+CiAgPGcgaWQ9InBhdGNoXzEiPgogICA8cGF0aCBk%0APSJNIDAgMjgwLjM4NTQ2NiAKTCAzNzAuNzE2MDE4IDI4MC4zODU0NjYgCkwg%0AMzcwLjcxNjAxOCAwIApMIDAgMCAKegoiIHN0eWxlPSJmaWxsOiNmZmZmZmY7%0AIi8+CiAgPC9nPgogIDxnIGlkPSJheGVzXzEiPgogICA8ZyBpZD0icGF0Y2hf%0AMiI+CiAgICA8cGF0aCBkPSJNIDMzLjM3OTA0MyAyNDUuMTQ2NTYyIApMIDMw%0AMS4yMTkwNDMgMjQ1LjE0NjU2MiAKTCAzMDEuMjE5MDQzIDI3LjcwNjU2MiAK%0ATCAzMy4zNzkwNDMgMjcuNzA2NTYyIAp6CiIgc3R5bGU9ImZpbGw6I2ZmZmZm%0AZjsiLz4KICAgPC9nPgogICA8ZyBpZD0iUGF0aENvbGxlY3Rpb25fMSI+CiAg%0AICA8cGF0aCBjbGlwLXBhdGg9InVybCgjcDY0ZDA1ZjkwM2YpIiBkPSJNIDI5%0AMi4xODU3NzQgMjQ0LjAxNjcyNiAKTCAyODguNDMxNjY1IDI0NC4wODExMDYg%0ACkwgMjg3LjIxMzQ0NCAyNDQuMTAxOTk3IApMIDI4My4zNTk4ODcgMjQ0LjE2%0AODA4MiAKTCAyODIuMjQxMTEzIDI0NC4xODcyNjggCkwgMjc4LjI4ODExIDI0%0ANC4yNTUwNTggCkwgMjc3LjI2ODc4MiAyNDQuMjcyNTM4IApMIDI3My4yMTYz%0AMzMgMjQ0LjM0MjAzNCAKTCAyNzIuMjk2NDUyIDI0NC4zNTc4MDkgCkwgMjY4%0ALjE0NDU1NSAyNDQuNDI5MDEgCkwgMjY3LjMyNDEyMSAyNDQuNDQzMDc5IApM%0AIDI2My4wNzI3NzggMjQ0LjUxNTk4NiAKTCAyNjIuMzUxNzkgMjQ0LjUyODM1%0AIApMIDI1OC4wMDEwMDEgMjQ0LjYwMjk2MiAKTCAyNTcuMzc5NDU5IDI0NC42%0AMTM2MjEgCkwgMjUyLjkyOTIyMyAyNDQuNjg5OTM4IApMIDI1Mi40MDcxMjkg%0AMjQ0LjY5ODg5MSAKTCAyNDcuODU3NDQ2IDI0NC43NzY5MTQgCkwgMjQ3LjQz%0ANDc5OCAyNDQuNzg0MTYyIApMIDI0Mi43ODU2NjkgMjQ0Ljg2Mzg5IApMIDI0%0AMi40NjI0NjcgMjQ0Ljg2OTQzMiAKTCAyMzcuNzEzODkxIDI0NC45NTA4NjYg%0ACkwgMjM3LjQ5MDEzNyAyNDQuOTU0NzAzIApMIDIzMi42NDIxMTQgMjQ1LjAz%0ANzg0MiAKTCAyMzIuNTE3ODA2IDI0NS4wMzk5NzMgCkwgMjI3LjU3MDMzNyAy%0ANDUuMTI0ODE4IApMIDIyNy41NDU0NzUgMjQ1LjEyNTI0NCAKTCAyMjYuMzAy%0AMzkzIDI0NS4xNDY1NjIgCkwgMjI3LjU1Nzc4MyAyNDUuMTQ2NTYyIApMIDIz%0AMi41NzkzNDUgMjQ1LjE0NjU2MiAKTCAyMzcuNjAwOTA2IDI0NS4xNDY1NjIg%0ACkwgMjQyLjYyMjQ2OCAyNDUuMTQ2NTYyIApMIDI0Ny42NDQwMyAyNDUuMTQ2%0ANTYyIApMIDI1Mi42NjU1OTEgMjQ1LjE0NjU2MiAKTCAyNTcuNjg3MTUzIDI0%0ANS4xNDY1NjIgCkwgMjYyLjcwODcxNSAyNDUuMTQ2NTYyIApMIDI2Ny43MzAy%0ANzcgMjQ1LjE0NjU2MiAKTCAyNzIuNzUxODM4IDI0NS4xNDY1NjIgCkwgMjc3%0ALjc3MzQgMjQ1LjE0NjU2MiAKTCAyODIuNzk0OTYyIDI0NS4xNDY1NjIgCkwg%0AMjg3LjgxNjUyMyAyNDUuMTQ2NTYyIApMIDI5Mi44MzgwODUgMjQ1LjE0NjU2%0AMiAKIiBzdHlsZT0iZmlsbDojN2UwM2ZmOyIvPgogICA8L2c+CiAgIDxnIGlk%0APSJQYXRoQ29sbGVjdGlvbl8yIj4KICAgIDxwYXRoIGNsaXAtcGF0aD0idXJs%0AKCNwNjRkMDVmOTAzZikiIGQ9Ik0gMjI2LjMwMjM5MyAyNDUuMTQ2NTYyIApM%0AIDIyNy41NDU0NzUgMjQ1LjEyNTI0NCAKTCAyMjcuNTcwMzM3IDI0NS4xMjQ4%0AMTggCkwgMjMyLjUxNzgwNiAyNDUuMDM5OTczIApMIDIzMi42NDIxMTQgMjQ1%0ALjAzNzg0MiAKTCAyMzcuNDkwMTM3IDI0NC45NTQ3MDMgCkwgMjM3LjcxMzg5%0AMSAyNDQuOTUwODY2IApMIDI0Mi40NjI0NjcgMjQ0Ljg2OTQzMiAKTCAyNDIu%0ANzg1NjY5IDI0NC44NjM4OSAKTCAyNDcuNDM0Nzk4IDI0NC43ODQxNjIgCkwg%0AMjQ3Ljg1NzQ0NiAyNDQuNzc2OTE0IApMIDI1Mi40MDcxMjkgMjQ0LjY5ODg5%0AMSAKTCAyNTIuOTI5MjIzIDI0NC42ODk5MzggCkwgMjU3LjM3OTQ1OSAyNDQu%0ANjEzNjIxIApMIDI1OC4wMDEwMDEgMjQ0LjYwMjk2MiAKTCAyNjIuMzUxNzkg%0AMjQ0LjUyODM1IApMIDI2My4wNzI3NzggMjQ0LjUxNTk4NiAKTCAyNjcuMzI0%0AMTIxIDI0NC40NDMwNzkgCkwgMjY4LjE0NDU1NSAyNDQuNDI5MDEgCkwgMjcy%0ALjI5NjQ1MiAyNDQuMzU3ODA5IApMIDI3My4yMTYzMzMgMjQ0LjM0MjAzNCAK%0ATCAyNzcuMjY4NzgyIDI0NC4yNzI1MzggCkwgMjc4LjI4ODExIDI0NC4yNTUw%0ANTggCkwgMjgyLjI0MTExMyAyNDQuMTg3MjY4IApMIDI4My4zNTk4ODcgMjQ0%0ALjE2ODA4MiAKTCAyODcuMjEzNDQ0IDI0NC4xMDE5OTcgCkwgMjg4LjQzMTY2%0ANSAyNDQuMDgxMTA2IApMIDI5Mi4xODU3NzQgMjQ0LjAxNjcyNiAKTCAyOTEu%0ANTMzNDY0IDI0Mi44ODY4OTEgCkwgMjg5LjA5NzAyMiAyNDIuOTI4Njc0IApM%0AIDI4Ni41NjExMzMgMjQyLjk3MjE2MiAKTCAyODQuMDI1MjQ0IDI0My4wMTU2%0ANSAKTCAyODEuNTg4ODAyIDI0My4wNTc0MzIgCkwgMjc4Ljk1MzQ2NyAyNDMu%0AMTAyNjI2IApMIDI3Ni42MTY0NzIgMjQzLjE0Mj "example")

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
~~~python
from ternary_diagram import ternary_diagram
~~~

### Make an instance
~~~python
materials = ['Li2O', 'LaO3', 'TiO2']
td = ternary_diagram(materials)
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
See also the example folder. (exampleフォルダも参照．)
```python
td = ternary_diagram(['Li2O', 'LaO3', 'TiO2'])
td.scatter([[1, 1, 1], [1, 2, 3]], z = [0, 1], marker = 'o')
td.plot([1, 1, 1], [1, 2, 3], color = 'black')
td.fig.savefig('figure.png', transparent = True, dpi = 300)
```
