from ternary_diagram import TernaryDiagram
import matplotlib.pyplot as plt

fig = plt.figure(facecolor = 'white', dpi = 100, figsize=(10, 4.8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.plot([0, 1], [0, 1], c = 'black')

materials = ['Li2O', 'La2O3', 'TiO2']
td = TernaryDiagram(materials, fig = fig, ax = ax2)
td.scatter([
    [1, 1, 1],
    ])
plt.tight_layout()
plt.show()