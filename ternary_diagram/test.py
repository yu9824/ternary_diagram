from ternary_diagram import TernaryDiagram
import matplotlib.pyplot as plt

materials = ['Li2O', 'La2O3', 'TiO2']
td = TernaryDiagram(materials)
td.scatter([
    [1, 1, 1],
    ])

plt.show()