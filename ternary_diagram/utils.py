from matplotlib.axes._subplots import Axes
import matplotlib.pyplot as plt
import numpy as np

def check_ax(ax):
    if ax is None:
        ax = plt.gca()
    elif isinstance(ax, Axes):
        ax = ax
    else:
        raise TypeError('`ax` is None or Axes object.\nThis `ax` is ({}).'.format(ax.__class__))
    return ax

def check_vector(vector, scale=True):
    """[summary]

    Parameters
    ----------
    vector : array | shape = (n, 3)
        ratio
    scale : bool, optional
        do minmaxscale or not, by default True

    Returns
    -------
    numpy.ndarray | shape = (n, 3)

    Raises
    ------
    ValueError
        when shape is not (n, 3)
    """
    vector = np.array(vector)
    if vector.shape[1] != 3:
        raise ValueError("`vector`'s shape must be (n, 3)")
    if scale:
        vector = vector / np.sum(vector, axis = 1, keepdims = True) # 今回keepdims = Trueは.reshape(-1, 1)と同義
    return vector

def three2two(vector):
    """
    Converted 3D proportions to 2D in order to generate a triangular diagram.

    Parameters
    ----------
    vector : array | shape = (n, 3)
        ratio

    Returns
    -------
    numpy.ndarray shape = (n, 2)
    """
    return (2 * vector[:, 2] + vector[:, 0]) / 2, np.sqrt(3) / 2 * vector[:, 0]

def get_label(compound_name):
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
        

    Raises
    ------
    ValueError
        when `compound_name` is not str.
    """
    if not isinstance(compound_name, str):
        raise ValueError('The `compound_name` must be string.')
    f = '$_{'
    b = '}$'
    N = len(compound_name)
    lst_compound_name = list(compound_name) + ['']   # outputするために変えていく．

    # １文字ずつ取り出して
    i = 0
    while i < N:
        l = compound_name[i] # l: letter
        if l.isdigit():
            j = i + 1
            while j < N + 1:
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
    return ''.join(lst_compound_name)
