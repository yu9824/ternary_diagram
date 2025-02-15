# deprecated in python>=3.9
from typing import Tuple  # isort: skip

from math import sqrt
from typing import Optional

import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike


def check_ax(ax: Optional[matplotlib.axes.Axes]) -> matplotlib.axes.Axes:
    """check ax

    Parameters
    ----------
    ax : None or Axes object
        if None, get current axes

    Returns
    -------
    Axes object

    Raises
    ------
    TypeError
        when ax is not None or Axes object
    """
    if ax is None:
        ax = plt.gca()
    elif isinstance(ax, matplotlib.axes.Axes):
        pass
    else:
        raise TypeError(
            "`ax` is None or Axes object.\nThis `ax` is ({}).".format(
                ax.__class__
            )
        )
    return ax


def check_2d_vector(vector: ArrayLike, scale: bool = True) -> np.ndarray:
    """check 2d vector

    Parameters
    ----------
    vector : ArrayLike | shape = (n, 3)
        ratio
    scale : bool, optional
        minmaxscale or not, by default True

    Returns
    -------
    numpy.ndarray | shape = (n, 3)

    Raises
    ------
    ValueError
        when shape is not (n, 3)
    """
    arr_vector = np.asarray(vector)
    if arr_vector.shape[1] != 3:
        raise ValueError("`vector`'s shape must be (n, 3)")
    if scale:
        arr_vector = arr_vector / np.sum(
            arr_vector, axis=1, keepdims=True
        )  # 今回keepdims = Trueは.reshape(-1, 1)と同義
    return arr_vector


def check_1d_vector(vector: ArrayLike, scale: bool = True) -> np.ndarray:
    """check 1d vector

    Parameters
    ----------
    vector : ArrayLike | shape = (3,)
        ratio
    scale : bool, optional
        minmaxscale or not, by default True

    Examples
    --------
    >>> check_1d_vector([1, 2, 3], scale=False)
    array([[1, 2, 3]])

    >>> check_1d_vector([2, 2, 4], scale=True)
    array([[0.25, 0.25, 0.5 ]])

    Returns
    -------
    np.ndarray | shape = (1, 3)
    """
    vector = np.array(vector).ravel()
    if len(vector) == 3:
        return check_2d_vector(np.array([vector]), scale=scale)
    else:
        raise ValueError("`vector`'s length must be 3.")


def three2two(vector: ArrayLike) -> Tuple[np.ndarray, np.ndarray]:
    """
    Converted 3D proportions to 2D in order to generate a triangular diagram.

    Parameters
    ----------
    vector : ArrayLike | shape = (n, 3)
        ratio

    Examples
    --------
    >>> three2two(check_2d_vector([[2, 2, 4]]))
    (array([0.625]), array([0.21650635]))

    Returns
    -------
    numpy.ndarray | shape = (n, 2)
    """
    arr_vector = np.asarray(vector)
    return (
        (2.0 * arr_vector[:, 2] + arr_vector[:, 0]) / 2.0,
        sqrt(3.0) / 2.0 * arr_vector[:, 0],
    )


def get_label(compound_name: str) -> str:
    """
    Convert the chemical composition to LaTeX notation.

    Parameters
    ----------
    compound_name : str
        A compound name, like 'Li2O'

    Returns
    -------
    str
        Chemical composition converted to LaTeX notation.

    Examples
    --------
    >>> get_label('Li2O')
    'Li$_{2}$O'

    >>> get_label('(LiLa)0.5TiO3')
    '(LiLa)$_{0.5}$TiO$_{3}$'

    Raises
    ------
    ValueError
        when `compound_name` is not str.
    """
    if not isinstance(compound_name, str):
        raise ValueError("The `compound_name` must be string.")

    f = "$_{"
    b = "}$"
    n_name = len(compound_name)

    # convert str to list
    # (add empty string to the end of the list to add b to the last letter.)
    lst_compound_name = list(compound_name) + [""]

    # find the number in the compound name.
    i = 0
    while i < n_name:
        # if you met a number, find the end of the number.
        letter = compound_name[i]
        if letter.isdigit():
            j = i + 1
            while j < n_name + 1:
                try:
                    float(compound_name[i:j])
                except ValueError:
                    break
                else:
                    j += 1
            j -= 1
            lst_compound_name[i] = f + lst_compound_name[i]
            lst_compound_name[j] = b + lst_compound_name[j]
            i = j
        i += 1
    return "".join(lst_compound_name)


if __name__ == "__main__":
    from doctest import testmod

    testmod(verbose=True)
