'''
Copyright © 2021 yu9824
'''

import numpy as np
import pandas as pd

from copy import deepcopy

import matplotlib.pyplot as plt
# import matplotlib.cm as cm      # ternary内にカラーマップを創設する
import matplotlib.tri as tri    # 三角図を簡単に出すやつ
try:
    # package
    from .utils import check_ax, check_vector, three2two, get_label
except:
    # for _test.py
    from utils import check_ax, check_vector, three2two, get_label

'''
    kwargs
z_max: colorbarの上限値を固定するかどうか．default;None
z_min: colorbarの上限値を固定するかどうか．default;None
norm: 標準化する必要があるかどうか．default;True
bar_label: colorbarの横に書くlabel名
'''

# default parameters
DEFAULT_CMAP = 'rainbow'
DEFAULT_ZORDER_CONTOUR = 0
DEFAULT_ZORDER_GRIDS = 1
DEFAULT_ZORDER_PLOTS = 2
DEFAULT_ZORDER_SCATTER = 3

class TernaryDiagram:
    def __init__(self, materials, ax=None):
        """
        Make instance.

        Create borders, etc. for triangulation diagrams.


        Parameters
        ----------
        materials : array (shape = (3,))
            A one-dimensional list of compounds that constitute an endpoint when generating a ternary_diagram.
        """

        # check `ax`
        self.ax = check_ax(ax)
        self.fig = self.ax.figure

        # Generate material_label (LaTeX notation)
        material_label = list(map(get_label, materials))

        # Allign the aspect
        self.ax.set_aspect('equal', 'datalim')

        # 目盛りや目盛りにつくラベルを表示しない
        self.ax.tick_params(labelbottom = False, labelleft = False, labelright = False, labeltop = False)
        self.ax.tick_params(bottom = False, left = False, right = False, top = False)

        # 枠線を表示しない．
        {self.ax.spines[position].set_visible(False) for position in ['bottom', 'left', 'right', 'top']}

        # h = √3/2
        h = np.sqrt(3.0)*0.5

        # 内側目盛
        inner_border_options = {
            'color': 'gray',
            'lw': 0.5,
            'zorder': DEFAULT_ZORDER_GRIDS,
        }
        for i in range(1,10):
            self.ax.plot([i/20.0, 1.0-i/20.0],[h*i/10.0, h*i/10.0], **inner_border_options)
            self.ax.plot([i/20.0, i/10.0],[h*i/10.0, 0.0], **inner_border_options)
            self.ax.plot([0.5+i/20.0, i/10.0],[h*(1.0-i/10.0), 0.0], **inner_border_options)

        # 外周の枠線
        outer_border_options = {
            'color': 'black',
            'lw': 2,
            'linestyle': '-',
            'zorder': DEFAULT_ZORDER_GRIDS,
            }
        self.ax.plot([0.0, 1.0],[0.0, 0.0], **outer_border_options)
        self.ax.plot([0.0, 0.5],[0.0, h], **outer_border_options)
        self.ax.plot([1.0, 0.5],[0.0, h], **outer_border_options)

        # 頂点のラベル
        font_size_material_label = 16
        self.ax.text(0.5, h+0.02, material_label[0], fontsize=font_size_material_label, ha = 'center', va = 'bottom')
        self.ax.text(0, -0.05, material_label[1], fontsize=font_size_material_label, ha = 'right', va = 'top')#, rotation=300)
        self.ax.text(1, -0.05, material_label[2], fontsize=font_size_material_label, ha = 'left', va = 'top')#, rotation=60)

        #軸ラベル
        font_size_axis_label = 10
        for i in range(1,10):
            self.ax.text(0.5+(10-i)/20.0, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize = font_size_axis_label, va = 'bottom', ha = 'left')
            self.ax.text((10-i)/20.0-0.01, h*(10-i)/10.0+0.04, '%d0' % i, fontsize = font_size_axis_label, rotation = 300, va = 'top', ha = 'right')
            self.ax.text(i/10.0+0.02, 0, '%d0' % i, fontsize = font_size_axis_label, rotation = 60, va = 'top', ha = 'right')

        # 二次元に変換したデータを保存しておく
        self.x = dict()
        self.y = dict()
    
    
    
    def scatter(self, vector, z=None, z_min=None, z_max=None, bar_label='', **kwargs):
        """
        Plot scatter points.

        Parameters
        ----------
        vector : array | shape = (n, 3)
            percentage of each compound mixed in 2D list / pandas.DataFrame / numpy.ndarray, where shape = [n, 3] (n is the number of samples to be plotted as integer)
        z : list, numpy.ndarray, pandas.Series etc, shape = (n,), optional
            , by default None
        z_min : int, float , optional
            , by default None
        z_max : int, float, optional
            , by default None
        bar_label : str, optional
            color bar label when `z` is not None., by default ''

        Returns
        -------
        Axes object
        """

        plotter = _ScatterPlotter(vector=vector, ax=self.ax, z=z, z_min=z_min, z_max=z_max, bar_label=bar_label, **kwargs)
        self._append_x_y(plotter)
        return self.ax

    def contour(self, vector, z, z_min=None, z_max=None, bar_label='', **kwargs):
        """
        To create a contour map.

        Parameters
        ----------
        vector : array | shape = (n, 3)
            percentage of each compound mixed in 2D list / pandas.DataFrame / numpy.ndarray, where shape = [n, 3] (n is the number of samples to be plotted as integer)
        z : list, numpy.ndarray, pandas.Series etc, shape = (n,)
            , by default None
        z_min : int, float, optional
            , by default None
        z_max : int, float, optional
            , by default None
        bar_label : str, optional
            color bar label when `z` is not None., by default ''

        Returns
        -------
        Axes object
        """

        plotter = _ContourPlotter(vector=vector, ax=self.ax, z=z, z_min=z_min, z_max=z_max, bar_label=bar_label, **kwargs)
        self._append_x_y(plotter)
        return self.ax

    def plot(self, r1, r2, **kwargs):   # 連結線を引く (scatterオブジェクトの使用が必須な状況)
        """
        To draw a tie line.

        Parameters
        ----------
        r1, r2 : array | shape = (3,)
            A mixing ratio of the compounds that are endpoints of the connecting line. A one-dimensional list of length 3.

        Returns
        -------
        Axes object
        """

        vector = np.array([r1, r2])
        plotter = _LinePlotter(vector=vector, ax=self.ax, **kwargs)
        self._append_x_y(plotter)
        return self.ax
    
    def _append_x_y(self, plotter):
        if not isinstance(plotter, _BasePlotter):
            raise TypeError()
        
        x, y = plotter.get_x_y()
        name = plotter.name
        if name in self.x:
            self.x[name].append(x)
            self.y[name].append(y)
        else:
            self.x[name] = [x]
            self.y[name] = [y]


class _BasePlotter:
    def __init__(self, vector, ax=None, z=None, z_min=None, z_max=None, bar_label='', **kwargs):
        # クラスオブジェクト
        self.vector = check_vector(vector)  # numpy.ndarray化
        self.ax = check_ax(ax)
        self.kwargs = kwargs
        self.z = np.array(z).ravel() if z is not None else None # convert to 1-d np.ndarray
        if self.z is not None:
            self.z_min = z_min
            self.z_max = z_max
            self.bar_label = bar_label

        self.name = 'base'  # change by each plotter

        # get_figure
        self.fig = self.ax.figure

        # 3次元ベクトルをx, y座標に落とし込む．
        self.x, self.y = three2two(self.vector)
        

    def colorbar(self):
        return self.fig.colorbar(self.triplot, shrink = 0.8, format='%.1f', label = self.bar_label, orientation = 'vertical', ticklocation = 'top', ax=self.ax)
    
    def tight_layout(self):
        return self.fig.tight_layout()
    
    def get_x_y(self):
        return self.x, self.y
    
    def _set_default_params(self, **kwargs):
        """
        set_default_params

        Examples
        --------------
        self._set_default_params(zorder=2)
        """
        for k, v in kwargs.items():
            if k not in self.kwargs:
                self.kwargs[k] = v


class _ScatterPlotter(_BasePlotter):
    def __init__(self, vector, ax=None, z=None, z_min=None, z_max=None, bar_label='', **kwargs):
        super().__init__(vector=vector, ax=ax, z=z, z_min=z_min, z_max=z_max, bar_label=bar_label, **kwargs)

        # name
        self.name = 'scatter'

        # default options
        self._set_default_params(
            zorder= DEFAULT_ZORDER_SCATTER,
        )

        # easy annotation 右上に簡易annotation
        self.annotations = self.kwargs.pop('annotations') if 'annotations' in self.kwargs else []
        for x, y, ann in zip(self.x, self.y, self.annotations):
            self.ax.annotate(ann, xy = (x, y), xytext = (x+0.02, y+0.02), fontsize = 8, color = '#262626')

        # when z is None
        if self.z is None:
            # To change color by each point
            self.ax.scatter(self.x, self.y, **self.kwargs)
            # for i_data in range(len(self.x)):
            #     self.ax.scatter(self.x[i_data], self.y[i_data], **self.kwargs)
        else:
            if 'cmap' not in self.kwargs:
                self.kwargs['cmap'] = DEFAULT_CMAP
            self.triplot = self.ax.scatter(self.x, self.y, c = self.z, vmin = self.z_min, vmax = self.z_max, **self.kwargs)
            self.colorbar()
        self.tight_layout()

class _ContourPlotter(_BasePlotter):
    def __init__(self, vector, ax=None, z=None, z_min=None, z_max=None, bar_label='', **kwargs):
        super().__init__(vector, ax=ax, z=z, z_min=z_min, z_max=z_max, bar_label=bar_label, **kwargs)

        # name
        self.name = 'contour'

        # default options
        self._set_default_params(
            cmap = DEFAULT_CMAP,
            zorder = DEFAULT_ZORDER_CONTOUR,
        )

        T = tri.Triangulation(self.x, self.y)
        # 等高線の線を引く場所，すなわち，色の勾配を表す配列．
        n_levels = 101  # 勾配をどれだけ細かくするかの変数．
        levels = np.linspace(self.z_min if self.z_min is not None else np.min(self.z), self.z_max if self.z_max is not None else np.max(self.z), n_levels)
        # solve issue#7
        unique = np.unique(levels)
        if unique.size == 1:
            offset = 0.001
            levels = np.linspace(unique[0] - offset * (n_levels // 2), unique[0] + offset * (n_levels // 2), n_levels)
        self.triplot = self.ax.tricontourf(self.x, self.y, T.triangles, self.z, levels = levels, **self.kwargs)

        self.colorbar()
        self.tight_layout()

class _LinePlotter(_BasePlotter):
    def __init__(self, vector, ax, **kwargs):
        super().__init__(vector, ax, **kwargs)

        # name
        self.name = 'plot'

        # default options
        self._set_default_params(
            zorder = DEFAULT_ZORDER_PLOTS,
        )

        # plot
        self.ax.plot(self.x, self.y, **self.kwargs)
        self.tight_layout()



if __name__ == '__main__':
    pass
