"""
Copyright © 2021 yu9824
"""
# deprecated from python>=3.9
from typing import Tuple, List

from abc import abstractmethod
from typing import Optional
from collections import defaultdict
from math import sqrt
from numbers import Number

from numpy.typing import ArrayLike
import numpy as np
import matplotlib.axes
import matplotlib.text
import matplotlib.collections
import matplotlib.lines
import matplotlib.colorbar

# import matplotlib.cm as cm      # ternary内にカラーマップを創設する
# 三角図を簡単に出すやつ
from matplotlib.tri.tricontour import TriContourSet
from matplotlib.tri.triangulation import Triangulation

from ternary_diagram.utils import (
    check_ax,
    check_1d_vector,
    check_2d_vector,
    three2two,
    get_label,
)


# default parameters
DEFAULT_CMAP = "rainbow"
DEFAULT_ZORDER_CONTOUR = 0
DEFAULT_ZORDER_GRIDS = 1
DEFAULT_ZORDER_PLOTS = 2
DEFAULT_ZORDER_SCATTER = 3


class TernaryDiagram:
    def __init__(
        self,
        materials: Tuple[str, str, str],
        ax: Optional[matplotlib.axes.Axes] = None,
    ) -> None:
        """
        Make instance.

        Create borders, etc. for triangulation diagrams.


        Parameters
        ----------
        materials : Tuple[str, str, str]
            A one-dimensional list of compounds that constitute an endpoint
             when generating a ternary_diagram.

        ax : Optional[matplotlib.axes.Axes], optional
            Axes object to draw a diagram. If None, automatically generate.


        Examples
        --------
        >>> from ternary_diagram import TernaryDiagram

        >>> # You can set `ax` to select which axes to draw.
        >>> # If not, the current axes will be used.
        >>> td = TernaryDiagram(["Li2O", "La2O3", "TiO2"])

        >>> # scatter
        >>> td.scatter(vector=[[1, 1, 1], [1, 2, 3]], z=[0, 1])
        >>> # You can set some options in `plt.scatter` like `marker`, `c` etc.
        >>> td.scatter([[2, 1, 3], [3, 2, 1]], marker="s", c="#022c5e", s=30)

        >>> # line plot
        >>> # You can set some options in `plt.plot` like `lw`, `c`, and so on.
        >>> td.plot([[1, 1, 1], [1, 2, 3]], color="black")

        >>> # save figure
        >>> td.fig.savefig("figure.png", dpi=144)

        """

        # check `ax`
        self.ax = check_ax(ax)
        self.fig = self.ax.figure

        # Generate material_label (LaTeX notation)
        material_label = tuple(map(get_label, materials))

        # Allign the aspect
        self.ax.set_aspect("equal", adjustable="datalim")

        # 目盛りや目盛りにつくラベルを表示しない
        self.ax.tick_params(
            labelbottom=False,
            labelleft=False,
            labelright=False,
            labeltop=False,
        )
        self.ax.tick_params(bottom=False, left=False, right=False, top=False)

        # clear borders
        for position in ("bottom", "left", "right", "top"):
            self.ax.spines[position].set_visible(False)

        # h = √3/2
        h = sqrt(3.0) / 2.0

        # inner tick marks
        inner_border_options = {
            "color": "gray",
            "lw": 0.5,
            "zorder": DEFAULT_ZORDER_GRIDS,
        }
        for i in range(1, 10):
            self.ax.plot(
                [i / 20.0, 1.0 - i / 20.0],
                [h * i / 10.0, h * i / 10.0],
                **inner_border_options
            )
            self.ax.plot(
                [i / 20.0, i / 10.0],
                [h * i / 10.0, 0.0],
                **inner_border_options
            )
            self.ax.plot(
                [0.5 + i / 20.0, i / 10.0],
                [h * (1.0 - i / 10.0), 0.0],
                **inner_border_options
            )

        # borders
        outer_border_options = {
            "color": "black",
            "lw": 2,
            "linestyle": "-",
            "zorder": DEFAULT_ZORDER_GRIDS,
        }
        self.ax.plot([0.0, 1.0], [0.0, 0.0], **outer_border_options)
        self.ax.plot([0.0, 0.5], [0.0, h], **outer_border_options)
        self.ax.plot([1.0, 0.5], [0.0, h], **outer_border_options)

        # 頂点のラベル (Labels of vertices)
        FONT_SIZE_MATERIAL_LABEL = 16
        # top label
        self.ax.text(
            0.5,
            h + 0.02,
            material_label[0],
            fontsize=FONT_SIZE_MATERIAL_LABEL,
            ha="center",
            va="bottom",
        )
        # left bottom label
        self.ax.text(
            0,
            -0.05,
            material_label[1],
            fontsize=FONT_SIZE_MATERIAL_LABEL,
            ha="right",
            va="top",
        )  # , rotation=300)
        # right bottom label
        self.ax.text(
            1,
            -0.05,
            material_label[2],
            fontsize=FONT_SIZE_MATERIAL_LABEL,
            ha="left",
            va="top",
        )  # , rotation=60)

        # 軸ラベル (Axis-label)
        FONT_SIZE_AXIS_LABEL = 10
        for i in range(1, 10):
            self.ax.text(
                0.5 + (10 - i) / 20.0,
                h * (1.0 - (10 - i) / 10.0),
                "%d0" % i,
                fontsize=FONT_SIZE_AXIS_LABEL,
                va="bottom",
                ha="left",
            )
            self.ax.text(
                (10 - i) / 20.0 - 0.01,
                h * (10 - i) / 10.0 + 0.04,
                "%d0" % i,
                fontsize=FONT_SIZE_AXIS_LABEL,
                rotation=300,
                va="top",
                ha="right",
            )
            self.ax.text(
                i / 10.0 + 0.02,
                0,
                "%d0" % i,
                fontsize=FONT_SIZE_AXIS_LABEL,
                rotation=60,
                va="top",
                ha="right",
            )

        # 二次元に変換したデータを保存しておく (Save the data converted to two dimensions)
        self.x_ = defaultdict(list)
        self.y_ = defaultdict(list)

    def scatter(
        self,
        vector: ArrayLike,
        z: Optional[ArrayLike] = None,
        z_min: Optional[Number] = None,
        z_max: Optional[Number] = None,
        annotations: Optional[List[str]] = None,
        flag_cbar: bool = True,
        **kwargs
    ) -> matplotlib.collections.PathCollection:
        """
        Plot scatter points.

        This is a wrapper of `matplotlib.pyplot.scatter`.

        Parameters
        ----------
        vector : array | shape = (n, 3)
            percentage of each compound mixed in 2D list / pandas.DataFrame
            / numpy.ndarray, where shape = [n, 3] (n is the number of samples)

        z : ArrayLike, shape = (n,), optional
            , by default None

        z_min : Optional[Number] , optional
            , by default None

        z_max : Optional[Number], optional
            , by default None

        annotations : Optional[List[str]], optional
            instance annotations, by default None
            if None, nothing is annotated.

        flag_cbar : bool, optional
            instance colorbar or not, by default True

        **kwargs : parameter of matplotlib.pyplot.scatter, optional
            For example, `marker='x'`, `facecolor='blue'` etc.

            See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html.   # noqa


        Returns
        -------
        matplotlib.collections.PathCollection
            A collection of scatter points.
        """

        plotter = _ScatterPlotter(
            vector=vector,
            ax=self.ax,
            z=z,
            z_min=z_min,
            z_max=z_max,
            annotations=annotations,
            flag_cbar=flag_cbar,
            **kwargs
        )
        self._append_x_y(plotter)
        return plotter.collection_

    def contour(
        self,
        vector: ArrayLike,
        z: Optional[ArrayLike] = None,
        z_min: Optional[Number] = None,
        z_max: Optional[Number] = None,
        flag_cbar: bool = True,
        **kwargs
    ) -> TriContourSet:
        """
        To create a contour map.

        Parameters
        ----------
        vector : ArrayLike | shape = (n, 3)
            percentage of each compound mixed in 2D list / pandas.DataFrame
            / numpy.ndarray, where shape = [n, 3] (n is the number of samples
            to be plotted as integer)

        z : Optional[ArrayLike], shape = (n,)
            , by default None
        z_min : Optional[Number], optional
            , by default None
        z_max : Optional[Number], optional
            , by default None
        **kwargs : parameter of matplotlib.pyplot.contour, optional
            https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html

        Returns
        -------
        matplotlib.tri.tricontour.TriContourSet
            A collection of contour lines.
        """

        plotter = _ContourPlotter(
            vector=vector,
            ax=self.ax,
            z=z,
            z_min=z_min,
            z_max=z_max,
            flag_cbar=flag_cbar,
            **kwargs
        )
        self._append_x_y(plotter)
        return plotter.collection_

    def plot(
        self, vector: ArrayLike, **kwargs
    ) -> List[matplotlib.lines.Line2D]:
        """
        To draw a tie line.

        This is a wrapper of `matplotlib.pyplot.plot`.

        Parameters
        ----------
        vector : array | shape = (n, 3)
            A mixing ratio of the compounds that are endpoints of
            the connecting line. A one-dimensional list of length 3.

        kwargs: parameter of matplotlib.pyplot.plot, optional
            See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html   # noqa


        Returns
        -------
        List[matplotlib.lines.Line2D]
            lines.
        """

        plotter = _LinePlotter(vector=vector, ax=self.ax, **kwargs)
        self._append_x_y(plotter)
        return plotter.collection_

    def annotate(
        self, text: str, vector: ArrayLike, **kwargs
    ) -> matplotlib.text.Annotation:
        """Annotate text.

        This is a wrapper of `matplotlib.pyplot.annotate`.

        Parameters
        ----------
        text : str
            Text to be displayed.

        vector : 1d array, whose length is 3.
            The position of the text to be displayed.

        kwargs : parameter of matplotlib.pyplot.annotate, optional
            see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html   # noqa


        Returns
        -------
        matplotlib.text.Annotation
            An annotation.
        """
        plotter = _AnnotatePlotter(text, vector, ax=self.ax, **kwargs)
        self._append_x_y(plotter)
        return plotter.collection_

    def colorbar(
        self,
        mappable,
        shrink=0.8,
        format="%.1f",
        label: str = "",
        orientation="vertical",
        ticklocation="top",
        **kwargs
    ) -> matplotlib.colorbar.Colorbar:
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
        return _draw_colorbar(
            mappable=mappable,
            ax=self.ax,
            shrink=shrink,
            format=format,
            label=label,
            orientation=orientation,
            ticklocation=ticklocation,
            **kwargs
        )

    def _append_x_y(self, plotter) -> None:
        """append x, y data

        Parameters
        ----------
        plotter : _BasePlotter
            plotter

        Raises
        ------
        TypeError
            "plotter must inherit `_BasePlotter`"
        """
        if not isinstance(plotter, _BasePlotter):
            raise TypeError("plotter must inherit `_BasePlotter`")

        name = plotter.name
        self.x_[name].append(plotter.x_)
        self.y_[name].append(plotter.y_)


class _BasePlotter:
    def __init__(
        self,
        vector: ArrayLike,
        ax: Optional[matplotlib.axes.Axes] = None,
        z: Optional[ArrayLike] = None,
        z_min: Optional[Number] = None,
        z_max: Optional[Number] = None,
        **kwargs
    ):
        """_BasePlotter

        This is a base class for the wrapper of `matplotlib.pyplot.` functions.

        Parameters
        ----------
        vector : ArrayLike
            vector
        ax : Optional[matplotlib.axes.Axes], optional
            , by default None
        z : Optional[ArrayLike], optional
            , by default None
        z_min : Optional[Number], optional
            , by default None
        z_max : Optional[Number], optional
            , by default None
        """
        self.vector: np.ndarray = check_2d_vector(vector)
        self.ax: matplotlib.axes.Axes = check_ax(ax)
        self.kwargs: dict = kwargs
        self.z: np.ndarray = (
            np.array(z).ravel() if z is not None else None
        )  # convert to 1-d np.ndarray

        # TODO: check
        if self.z is not None:
            self.z_min = z_min
            self.z_max = z_max

        # get_figure
        self.fig = self.ax.figure

        # 3次元ベクトルをx, y座標に落とし込む．
        self.__x, self.__y = three2two(self.vector)

    def _set_default_params(self, **kwargs):
        """
        set default params

        Examples
        --------------
        >>> self._set_default_params(zorder=2)
        """
        for k, v in kwargs.items():
            if k not in self.kwargs:
                self.kwargs[k] = v

    @property
    def x_(self) -> np.ndarray:
        # TODO: docstring
        return self.__x

    @x_.setter
    def x_(self, _x):
        raise AttributeError("x_ is read-only")

    @property
    def y_(self) -> np.ndarray:
        # TODO: docstring
        return self.__y

    @y_.setter
    def y_(self, _y):
        raise AttributeError("y_ is read-only")

    @property
    @abstractmethod
    def name(self) -> str:
        """Plotter name"""
        ...

    @name.setter
    def name(self, _v):
        raise AttributeError("name is read-only")

    @property
    def collection_(self):
        return self.__collection

    @collection_.setter
    def collection_(self, _collection):
        self.__collection = _collection


class _ScatterPlotter(_BasePlotter):
    def __init__(
        self,
        vector,
        ax=None,
        z=None,
        z_min=None,
        z_max=None,
        annotations=None,
        flag_cbar: bool = True,
        **kwargs
    ):
        super().__init__(
            vector=vector, ax=ax, z=z, z_min=z_min, z_max=z_max, **kwargs
        )

        # default options
        self._set_default_params(
            zorder=DEFAULT_ZORDER_SCATTER,
        )

        # easy annotation 右上に簡易annotation
        if annotations is not None:
            assert len(annotations) == len(
                self.x_
            ), "len(annotations) != len(x)"
            for x, y, txt in zip(self.x_, self.y_, annotations):
                txt = get_label(txt)
                self.ax.annotate(
                    txt,
                    xy=(x, y),
                    xytext=(x + 0.02, y + 0.02),
                    fontsize=8,
                    color="#262626",
                )

        # when z is None
        if self.z is None:
            flag_cbar = False
            # To change color by each point
            self.collection_ = self.ax.scatter(self.x_, self.y_, **self.kwargs)
            # for i_data in range(len(self.x_)):
            #     self.ax.scatter(self.x_[i_data], self.y_[i_data], **self.kwargs)    # noqa
        else:
            if "cmap" not in self.kwargs:
                self.kwargs["cmap"] = DEFAULT_CMAP
            self.collection_ = self.ax.scatter(
                self.x_,
                self.y_,
                c=self.z,
                vmin=self.z_min,
                vmax=self.z_max,
                **self.kwargs
            )
            if flag_cbar:
                self.colorbar = _draw_colorbar(self.collection_, ax=self.ax)
        self.fig.tight_layout()

    @property
    def name(self):
        return "scatter"


class _ContourPlotter(_BasePlotter):
    def __init__(
        self,
        vector,
        ax=None,
        z=None,
        z_min=None,
        z_max=None,
        flag_cbar: bool = True,
        **kwargs
    ):
        super().__init__(
            vector, ax=ax, z=z, z_min=z_min, z_max=z_max, **kwargs
        )

        # default options
        self._set_default_params(
            cmap=DEFAULT_CMAP,
            zorder=DEFAULT_ZORDER_CONTOUR,
        )

        triangulation = Triangulation(self.x_, self.y_)
        # 等高線の線を引く場所，すなわち，色の勾配を表す配列．
        N_LEVELS = 101  # 勾配をどれだけ細かくするかの変数．
        levels = np.linspace(
            self.z_min if self.z_min is not None else np.min(self.z),
            self.z_max if self.z_max is not None else np.max(self.z),
            N_LEVELS,
        )
        # solve issue#7
        unique = np.unique(levels)
        if unique.size == 1:
            OFFSET = 0.001
            levels = np.linspace(
                unique[0] - OFFSET * (N_LEVELS // 2),
                unique[0] + OFFSET * (N_LEVELS // 2),
                N_LEVELS,
            )
        self.collection_ = self.ax.tricontourf(
            self.x_,
            self.y_,
            triangulation.get_masked_triangles(),
            self.z,
            levels=levels,
            **self.kwargs
        )
        if flag_cbar:
            self.colorbar = _draw_colorbar(
                mappable=self.collection_, ax=self.ax
            )
        self.fig.tight_layout()

    @property
    def name(self):
        return "contour"


class _LinePlotter(_BasePlotter):
    def __init__(self, vector, ax=None, **kwargs):
        super().__init__(
            vector, ax=ax, z=None, z_min=None, z_max=None, **kwargs
        )

        # default options
        self._set_default_params(
            zorder=DEFAULT_ZORDER_PLOTS,
        )

        # plot
        self.collection_: List[matplotlib.lines.Line2D] = self.ax.plot(
            self.x_, self.y_, **self.kwargs
        )
        self.fig.tight_layout()

    @property
    def name(self):
        return "plot"


class _AnnotatePlotter(_BasePlotter):
    def __init__(self, text, vector, ax=None, **kwargs):
        vector = check_1d_vector(vector, scale=False)
        super().__init__(
            vector, ax=ax, z=None, z_min=None, z_max=None, **kwargs
        )

        if "xytext" not in kwargs:
            kwargs["xytext"] = (self.x_[0] + 0.02, self.y_[0] + 0.02)
        if "fontsize" not in kwargs:
            kwargs["fontsize"] = 8

        # check_text
        try:
            text = get_label(text)
        except ValueError:
            pass
        # annotate
        self.collection_ = self.ax.annotate(
            text=text, xy=(self.x_[0], self.y_[0]), **kwargs
        )

        self.fig.tight_layout()

    @property
    def name(self):
        return "annotate"


def _draw_colorbar(
    mappable,
    ax: Optional[matplotlib.axes.Axes] = None,
    shrink=0.8,
    format="%.1f",
    label: str = "",
    orientation="vertical",
    location="right",
    **kwargs
) -> matplotlib.colorbar.Colorbar:
    """Draw a colorbar.

    This is a wrapper of `matplotlib.pyplot.colorbar`.

    Parameters
    ----------
    mappable :
        mapplotable object
    ax : Optional[matplotlib.axes.Axes], optional
        axes, by default None
    shrink : float, optional
        , by default 0.8
    format : str, optional
        , by default "%.1f"
    label : str, optional
        , by default ""
    orientation : str, optional
        , by default "vertical"
    location : str, optional
        , by default "right"

    Returns
    -------
    matplotlib.colorbar.Colorbar
        colorbar object
    """
    # check ax
    ax = check_ax(ax)

    # draw colorbar
    return ax.figure.colorbar(
        mappable,
        ax=ax,
        shrink=shrink,
        format=format,
        label=label,
        orientation=orientation,
        location=location,
        **kwargs
    )


if __name__ == "__main__":
    pass
