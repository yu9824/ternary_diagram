from matplotlib.axes._subplots import Axes
import matplotlib.pyplot as plt

def check_ax(ax):
    if ax is None:
        ax = plt.gca()
    elif isinstance(ax, Axes):
        ax = ax
    else:
        raise TypeError('`ax` is None or Axes object.\nThis `ax` is ({}).'.format(ax.__class__))
    return ax