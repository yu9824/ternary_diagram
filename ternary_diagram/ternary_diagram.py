import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.cm as cm      #ternary内にカラーマップを創設する
import matplotlib.tri as tri    # 三角図を簡単に出すやつ

'''
    options
maximum: colorbarの上限値を固定するかどうか．default;None
minimum: colorbarの上限値を固定するかどうか．default;None
norm: 標準化する必要があるかどうか．default;True
mode: 'scatter' or 'contour'
bar_label: colorbarの横に書くlabel名
color: 一種類のscatterのときの色
'''

def ternary_diagram(reactant, vector, **options):
    def grid(reactant, fig, ax):
        ax1 = ax
        # 本当はここにreactant_labelを作成するプログラム作りたい
        def get_label(name):
            lst_name = list(name)
            for i, s in enumerate(name):
                if s.isdigit():
                    lst_name[i - 1] += '$_{'
                    for j in range(i, len(name)):
                        if name[j].isupper():
                            lst_name[j - 1] += '}$'
                            break
                    else:
                        lst_name[-1] += '}$'
            return ''.join(lst_name)
        reactant_label = list(map(get_label, reactant))


        # fig = plt.figure()
        # ax1 = fig.add_subplot(111)
        ax1.set_aspect('equal', 'datalim')
        plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
        plt.tick_params(bottom=False, left=False, right=False, top=False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)

        h = np.sqrt(3.0)*0.5

        #内側目盛
        for i in range(1,10):
            ax1.plot([i/20.0, 1.0-i/20.0],[h*i/10.0, h*i/10.0], color = 'gray', lw = 0.5)
            ax1.plot([i/20.0, i/10.0],[h*i/10.0, 0.0], color = 'gray', lw = 0.5)
            ax1.plot([0.5+i/20.0, i/10.0],[h*(1.0-i/10.0), 0.0], color = 'gray', lw = 0.5)

        #外周
        ax1.plot([0.0, 1.0],[0.0, 0.0], 'k-', lw = 2)
        ax1.plot([0.0, 0.5],[0.0, h], 'k-', lw = 2)
        ax1.plot([1.0, 0.5],[0.0, h], 'k-', lw = 2)

        #頂点のラベル
        ax1.text(0.5, h+0.02, reactant_label[0], fontsize=16, ha = 'center', va = 'bottom')
        ax1.text(0, -0.05, reactant_label[1], fontsize=16, ha = 'right', va = 'top')#, rotation=300)
        ax1.text(1, -0.05, reactant_label[2], fontsize=16, ha = 'left', va = 'top')#, rotation=60)

        #軸ラベル
        for i in range(1,10):
            ax1.text(0.5+(10-i)/20.0, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize = 10)
            ax1.text((10-i)/20.0-0.06, h*(10-i)/10.0+0.02, '%d0' % i, fontsize = 10, rotation = 300)
            ax1.text(i/10.0-0.03, -0.07, '%d0' % i, fontsize = 10, rotation = 60)

        return fig, ax1


    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig, ax = grid(reactant, fig, ax)

    vector = np.array(vector)

    norm = options['norm'] if 'norm' in options else True
    if norm:
        # vectorの正規化
        vector = vector / np.sum(vector, axis = 1, keepdims = True) # 今回keepdims = Trueは.reshape(-1, 1)と同義

    x, y = (2 * vector[:, 2] + vector[:, 0]) / 2, np.sqrt(3) / 2 * vector[:, 0] # 3次元ベクトルをx, y座標に落とし込む．

    z = np.array(options['z']).flatten() if 'z' in options else None    # 念のためzをnp.ndarrayにしてflatten

    if z is None:
        color = options['color'] if 'color' in options else 'blue'
        plt.scatter(x, y, c = color)
    else:
        maximum = options['maximum'] if 'maximum' in options else np.max(z) + (np.max(z) - np.min(z)) * 0.05
        minimum = options['minimum'] if 'minimum' in options else np.min(z) - (np.max(z) - np.min(z)) * 0.05
        bl = options['bar_label'] if 'bar_label' in options else ''
        mode = options['mode'] if 'mode' in options else 'scatter'

        if mode == 'contour':
            T = tri.Triangulation(x, y)
            triplot = plt.tricontourf(x, y, T.triangles, z, np.linspace(minimum, maximum, 101), cmap = 'rainbow')
        elif mode == 'scatter':
            triplot = plt.scatter(x, y, c = z, cmap = 'rainbow', vmin = minimum, vmax = maximum)

        plt.colorbar(triplot, shrink = 0.8, format='%.1f', label = bl, orientation = 'vertical', ticklocation = 'top')

    return fig

if __name__ == '__main__':
    df = pd.read_csv('example/scatter/example_scatter.csv')
    fig = ternary_diagram(df.columns[0:-1], df.iloc[:, 0:-1])
    plt.show()
