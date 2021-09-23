
if __name__ == '__main__':
    from ternary_diagram import TernaryDiagram
    import matplotlib.pyplot as plt
    import pandas as pd
    from element_recognition import make_compositions

    n_cols = 3
    n_rows = 1
    fig, axes = plt.subplots(n_rows, n_cols, facecolor = 'white', dpi = 72, figsize=(6.4*n_cols, 4.8*n_rows))

    # print(plt.gca() == ax2, plt.gca() == ax1)

    df_mono_scatter = pd.read_csv('https://raw.githubusercontent.com/yu9824/ternary_diagram/main/example/mono_scatter/example_mono_scatter.csv')
    df_scatter = pd.read_csv('https://raw.githubusercontent.com/yu9824/ternary_diagram/main/example/scatter/example_scatter.csv')
    df_contour = pd.read_csv('https://raw.githubusercontent.com/yu9824/ternary_diagram/main/example/contour/example_contour.csv')

    tds = []
    for i in range(2):
        tds.append(TernaryDiagram(materials = df_mono_scatter.columns, ax=axes[i]))
    tds.append(TernaryDiagram(materials=df_contour.columns[:3], ax=axes[2]))

    # td.scatter([
    #     [1, 1, 1],
    #     ])
    tds[0].scatter(df_mono_scatter)
    tds[0].annotate('sample', df_mono_scatter.iloc[0])

    # tds[1].scatter(df_mono_scatter, color='black', zorder=1, annotations=make_compositions(df_mono_scatter.columns, ratio=df_mono_scatter).index)
    tds[1].scatter(df_mono_scatter, color='black', zorder=1, annotations=df_mono_scatter.index)
    tds[1].plot([[0, 1, 9], [1, 0, 9]], c='gray', lw=2, zorder=0)

    tds[2].contour(df_contour.iloc[:, 0:3], df_contour['z'])
    tds[2].scatter(df_scatter.iloc[:, 0:3], df_scatter['z'])
    fig.tight_layout()
    plt.show()
    plt.close()

    # print(tds[2].x, tds[2].y)