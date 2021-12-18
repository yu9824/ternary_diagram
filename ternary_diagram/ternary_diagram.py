'''
Copyright © 2021 yu9824
'''

from typing import Optional

import numpy as np
import matplotlib
from copy import deepcopy
import matplotlib.pyplot as plt
# import matplotlib.cm as cm      # ternary内にカラーマップを創設する
import matplotlib.tri as tri    # 三角図を簡単に出すやつ
try:
    # package
    from .utils import check_ax, check_1d_vector, check_2d_vector, three2two, get_label
except:
    # for _test.py
    from utils import check_ax, check_1d_vector, check_2d_vector, three2two, get_label

'''
    kwargs
z_max: colorbarの上限値を固定するかどうか．default;None
z_min: colorbarの上限値を固定するかどうか．default;None
norm: 標準化する必要があるかどうか．default;True
'''

# default parameters
DEFAULT_CMAP = 'rainbow'
DEFAULT_ZORDER_CONTOUR = 0
DEFAULT_ZORDER_GRIDS = 1
DEFAULT_ZORDER_PLOTS = 2
DEFAULT_ZORDER_SCATTER = 3

class TernaryDiagram:
    def __init__(self, materials, ax: Optional[matplotlib.axes.Axes]=None):
        """
        Make instance.

        Create borders, etc. for triangulation diagrams.


        Parameters
        ----------
        materials : array (shape = (3,))
            A one-dimensional list of compounds that constitute an endpoint when generating a ternary_diagram.
        ax : matplotlib.axes.Axes, optional
            Axes object to draw a diagram. If None, automatically generate.
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
    
    
    
    def scatter(self, vector, z=None, z_min=None, z_max=None, annotations=None, flag_cbar:bool = True, **kwargs) -> matplotlib.collection.PathCollection:
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
        annotations : array, optional
            to add annotation easily, by default None
        **kwargs : parameter of matplotlib.pyplot.scatter, optional
            For example, `marker='x'`, `facecolor='blue'` etc.
            
            See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html.
        

        Returns
        -------
        matplotlib.collection.PathCollection
            A collection of scatter points.
        """

        plotter = _ScatterPlotter(vector=vector, ax=self.ax, z=z, z_min=z_min, z_max=z_max, annotations=annotations, flag_cbar=flag_cbar, **kwargs)
        self._append_x_y(plotter)
        return plotter._return_

    def contour(self, vector, z, z_min=None, z_max=None, flag_cbar:bool = True, **kwargs) -> matplotlib.tri.TriContourSet:
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
        **kwargs : parameter of matplotlib.pyplot.contour, optional
            https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html

        Returns
        -------
        matplotlib.tri.TriContourSet
            A collection of contour lines.
        """

        plotter = _ContourPlotter(vector=vector, ax=self.ax, z=z, z_min=z_min, z_max=z_max, flag_cbar=flag_cbar, **kwargs)
        self._append_x_y(plotter)
        return plotter._return_

    def plot(self, vector, **kwargs) -> matplotlib.lines.Line2D:
        """
        To draw a tie line.

        Parameters
        ----------
        vector : array | shape = (n, 3)
            A mixing ratio of the compounds that are endpoints of the connecting line. A one-dimensional list of length 3.
        **kwargs: parameter of matplotlib.pyplot.plot, optional
            See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html


        Returns
        -------
        matplotlib.lines.Line2D
            A line.
        """

        plotter = _LinePlotter(vector=vector, ax=self.ax, **kwargs)
        self._append_x_y(plotter)
        return plotter._return_
    
    def annotate(self, text:str, vector, **kwargs) -> matplotlib.text.Annnotation:
        """annotate

        Parameters
        ----------
        text : str
            
        vector : 1d array, whose length is 3.
            

        Returns
        -------
        matplotlib.text.Annnotation
            An annotation.
        """
        plotter = _AnnotatePlotter(text, vector, ax=self.ax, **kwargs)
        self._append_x_y(plotter)
        return plotter._return_
    
    def colorbar(self, mappable, shrink = 0.8, format = '%.1f', label:str = '', orientation = 'vertical', ticklocation = 'top', **kwargs)->matplotlib.colorbar.Colorbar:
        """Draw a colorbar.

        Parameters
        ----------
        mappable : matplotlib.cm.ScalarMappable
            The object that contains the colorbar data.
        shrink : float, optional
            how much to shrink the colorbar, by default 0.8
        format : str, optional
            float format, by default '%.1f'
        label : str, optional
            bar label, by default ''
        orientation : str, optional
            bar orientation, by default 'vertical'
        ticklocation : str, optional
            tick location, by default 'top'

        Returns
        -------
        matplotlib.colorbar.Colorbar
            colorbar object
        """        
        return _draw_colorbar(mappable=mappable, ax=self.ax, shrink=shrink, format=format, label=label, orientation=orientation, ticklocation=ticklocation, **kwargs)
    
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
    def __init__(self, vector, ax=None, z=None, z_min=None, z_max=None, **kwargs):
        # クラスオブジェクト
        self.vector:np.ndarray = check_2d_vector(vector)  # numpy.ndarray化
        self.ax:matplotlib.axes.Axes = check_ax(ax)
        self.kwargs:dict = kwargs
        self.z:np.ndarray = np.array(z).ravel() if z is not None else None # convert to 1-d np.ndarray
        if self.z is not None:
            self.z_min = z_min
            self.z_max = z_max

        # change by each plotter
        self.name:str = 'base'
        self._return_ = None

        # get_figure
        self.fig = self.ax.figure

        # 3次元ベクトルをx, y座標に落とし込む．
        self.x, self.y = three2two(self.vector)
    
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
    def __init__(self, vector, ax=None, z=None, z_min=None, z_max=None, annotations = None, flag_cbar:bool = True, **kwargs):
        super().__init__(vector=vector, ax=ax, z=z, z_min=z_min, z_max=z_max, **kwargs)

        # name
        self.name = 'scatter'

        # default options
        self._set_default_params(
            zorder= DEFAULT_ZORDER_SCATTER,
        )

        # easy annotation 右上に簡易annotation
        if annotations is not None:
            for x, y, txt in zip(self.x, self.y, annotations):
                try:
                    txt = get_label(txt)
                except ValueError:
                    pass
                self.ax.annotate(txt, xy = (x, y), xytext = (x+0.02, y+0.02), fontsize = 8, color = '#262626')

        # when z is None
        if self.z is None:
            flag_cbar = False
            # To change color by each point
            self._return_ = self.ax.scatter(self.x, self.y, **self.kwargs)
            # for i_data in range(len(self.x)):
            #     self.ax.scatter(self.x[i_data], self.y[i_data], **self.kwargs)
        else:
            if 'cmap' not in self.kwargs:
                self.kwargs['cmap'] = DEFAULT_CMAP
            self._return_ = self.ax.scatter(self.x, self.y, c = self.z, vmin = self.z_min, vmax = self.z_max, **self.kwargs)
            if flag_cbar:
                _draw_colorbar(self._return_, ax=self.ax)
        self.fig.tight_layout()

class _ContourPlotter(_BasePlotter):
    def __init__(self, vector, ax=None, z=None, z_min=None, z_max=None, flag_cbar:bool=True, **kwargs):
        super().__init__(vector, ax=ax, z=z, z_min=z_min, z_max=z_max, **kwargs)

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
        self._return_ = self.ax.tricontourf(self.x, self.y, T.triangles, self.z, levels = levels, **self.kwargs)
        if flag_cbar:
            self.colorbar = _draw_colorbar(mappable=self._return_, ax=self.ax)
        self.fig.tight_layout()

class _LinePlotter(_BasePlotter):
    def __init__(self, vector, ax=None, **kwargs):
        super().__init__(vector, ax=ax, z=None, z_min=None, z_max=None, **kwargs)

        # name
        self.name = 'plot'

        # default options
        self._set_default_params(
            zorder = DEFAULT_ZORDER_PLOTS,
        )

        # plot
        self._return_ = self.ax.plot(self.x, self.y, **self.kwargs)
        self.fig.tight_layout()

class _AnnotatePlotter(_BasePlotter):
    def __init__(self, text, vector, ax=None, **kwargs):
        vector = check_1d_vector(vector, scale=False)
        super().__init__(vector, ax=ax, z=None, z_min=None, z_max=None, **kwargs)

        # name
        self.name = 'annotate'

        if 'xytext' not in kwargs:
            kwargs['xytext'] = (self.x[0] + 0.02, self.y[0] + 0.02)
        if 'fontsize' not in kwargs:
            kwargs['fontsize'] = 8

        # check_text
        try:
            text = get_label(text)
        except ValueError:
            pass
        # annotate
        self._return_ = self.ax.annotate(text=text, xy=(self.x[0], self.y[0]), **kwargs)

        self.fig.tight_layout()


def _draw_colorbar(mappable, ax:matplotlib.axes.Axes = None, shrink = 0.8, format = '%.1f', label:str = '', orientation = 'vertical', ticklocation = 'top', **kwargs)->matplotlib.colorbar.Colorbar:
    if ax is None:
        ax = plt.gca()
    return ax.figure.colorbar(mappable, ax=ax, shrink=shrink, format=format, label=label, orientation=orientation, ticklocation=ticklocation, **kwargs)


if __name__ == '__main__':
    pass
