import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.cm as cm      # ternary内にカラーマップを創設する
import matplotlib.tri as tri    # 三角図を簡単に出すやつ

'''
    options
maximum: colorbarの上限値を固定するかどうか．default;None
minimum: colorbarの上限値を固定するかどうか．default;None
norm: 標準化する必要があるかどうか．default;True
mode: 'scatter' or 'contour'
bar_label: colorbarの横に書くlabel名
'''

class ternary_diagram:
    def __init__(self, reactant):
        # 単色scatterのときにcolormapのうち何番目までを使ったかを保存しておく変数とcolormapの指定
        self.color_counta = 0
        self.mono_cmap = plt.get_cmap('Set1')

        # figure, axisオブジェクトの生成
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        # reactant_labelを生成する関数を定義し， 生成
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

        # 正方形にする
        self.ax.set_aspect('equal', 'datalim')

        # 目盛りや目盛りにつくラベルを表示しない
        self.ax.tick_params(labelbottom = False, labelleft = False, labelright = False, labeltop = False)
        self.ax.tick_params(bottom = False, left = False, right = False, top = False)

        # 枠線を表示しない．
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)

        # h = √3/2
        h = np.sqrt(3.0)*0.5

        # 内側目盛
        line_options = {'color':'gray', 'lw':0.5, 'zorder':1}
        for i in range(1,10):
            self.ax.plot([i/20.0, 1.0-i/20.0],[h*i/10.0, h*i/10.0], **line_options)
            self.ax.plot([i/20.0, i/10.0],[h*i/10.0, 0.0], **line_options)
            self.ax.plot([0.5+i/20.0, i/10.0],[h*(1.0-i/10.0), 0.0], **line_options)

        # 外周の枠線
        self.ax.plot([0.0, 1.0],[0.0, 0.0], 'k-', lw = 2)
        self.ax.plot([0.0, 0.5],[0.0, h], 'k-', lw = 2)
        self.ax.plot([1.0, 0.5],[0.0, h], 'k-', lw = 2)

        # 頂点のラベル
        self.ax.text(0.5, h+0.02, reactant_label[0], fontsize=16, ha = 'center', va = 'bottom')
        self.ax.text(0, -0.05, reactant_label[1], fontsize=16, ha = 'right', va = 'top')#, rotation=300)
        self.ax.text(1, -0.05, reactant_label[2], fontsize=16, ha = 'left', va = 'top')#, rotation=60)

        #軸ラベル
        for i in range(1,10):
            self.ax.text(0.5+(10-i)/20.0, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize = 10)
            self.ax.text((10-i)/20.0-0.06, h*(10-i)/10.0+0.02, '%d0' % i, fontsize = 10, rotation = 300)
            self.ax.text(i/10.0-0.03, -0.07, '%d0' % i, fontsize = 10, rotation = 60)

    # *** サブ関数 ***
    def _get_from_options(self, options, key, default):
        return options[key] if key in options else default

    def _three2two(self, vector):
        return (2 * vector[:, 2] + vector[:, 0]) / 2, np.sqrt(3) / 2 * vector[:, 0]

    class _common:
        def __init__(self, outer, vector, **options):
            # numpy.ndarray化
            self.vector = np.array(vector)

            # 正規化するかどうか．
            norm = outer._get_from_options(options, 'norm', True)
            if norm:
                # self.vectorの正規化
                self.vector = self.vector / np.sum(self.vector, axis = 1, keepdims = True) # 今回keepdims = Trueは.reshape(-1, 1)と同義

            # 3次元ベクトルをx, y座標に落とし込む．
            # self.x, self.y = (2 * self.vector[:, 2] + self.vector[:, 0]) / 2, np.sqrt(3) / 2 * self.vector[:, 0]
            self.x, self.y = outer._three2two(self.vector)

            # 念のためself.zをnp.ndarrayにしてflatten
            self.z = np.array(options['z']).flatten() if 'z' in options else None

            if self.z is not None:
                self.maximum = options['maximum'] if 'maximum' in options else None
                self.minimum = options['minimum'] if 'minimum' in options else None
                self.bl = options['bar_label'] if 'bar_label' in options else ''

        def colorbar(self):
            plt.colorbar(self.triplot, shrink = 0.8, format='%.1f', label = self.bl, orientation = 'vertical', ticklocation = 'top')


    class _scatter_(_common):
        def __init__(self, outer, vector, **options):   # なぜか**kwargsで継承クラスの初期化メソッドともども使うとダメだった．
            super().__init__(outer, vector, **options)   # ternary_diagramクラスのselfを引数として与えている．

            marker = options['marker'] if 'marker' in options else 'o'
            # zに値が指定されていないとき
            zorder = 2
            if self.z is None:
                # 色について (単色なのは zがNoneのときだけなので)
                if 'c' in options:
                    outer.color = options['c']
                elif 'color' in options:
                    outer.color = options['color']
                else:
                    outer.color = outer.mono_cmap(outer.color_counta)    # 各点ごとに色を指定するのが普通っぽいので， 点の数分で二次元化
                    outer.color_counta += 1

                outer.ax.scatter(self.x, self.y, c = [outer.color for _ in range(len(vector))], zorder = zorder)
            else:
                self.triplot = outer.ax.scatter(self.x, self.y, c = self.z, cmap = 'rainbow', vmin = self.minimum, vmax = self.maximum, zorder = zorder)
                self.colorbar()

    class _contour_(_common):
        def __init__(self, outer, vector, **options):   # なぜか**kwargsで継承クラスの初期化メソッドともども使うとダメだった．
            super().__init__(outer, vector, **options)   # ternary_diagramクラスのselfを引数として与えている．

            T = tri.Triangulation(self.x, self.y)
            self.triplot = plt.tricontourf(self.x, self.y, T.triangles, self.z, np.linspace(self.minimum if self.minimum is not None else np.min(self.z), self.maximum if self.maximum is not None else np.max(self.z), 101), cmap = 'rainbow')
            self.colorbar()

    class _plot_(_common):
        def __init__(self, outer, vector, **options):
            super().__init__(outer, vector, **options)

            # 3次元を2次元に．
            x, y = outer._three2two(self.vector)

            plot_options = {'color':outer.color, 'zorder':1}
            #option系
            if 'linewidth' in options:
                plot_options['linewidth'] = options['linewidth']
            elif 'lw' in options:
                plot_options['lw'] = options['lw']
            else:
                plot_options['lw'] = 1

            # plot
            outer.ax.plot(x, y, **plot_options)

    def scatter(self, vector, **options):
        self._scatter_(self, vector, **options) # selfオブジェクトを渡してる．

    def contour(self, vector, **options):
        self._contour_(self, vector, **options)# selfオブジェクトを渡してる．

    def plot(self, r1, r2, **options):   # 連結線を引く (scatterオブジェクトの使用が必須な状況)
        vector = np.array([r1, r2])
        self._plot_(self, vector, **options)



if __name__ == '__main__':
    df = pd.read_csv('example/scatter/example_scatter.csv')
    # fig = ternary_diagram(df.columns[0:-1], df.iloc[:, 0:-1])
    # plt.show()

    td = ternary_diagram(['Li2O', 'La2O3', 'TiO2'])

    # N = 1000
    # td.contour(np.random.rand(3 * N).reshape(N, 3), z = np.random.rand(N))
    # td.scatter([[6, 1, 3]], z = [1])
    td.scatter([[1, 2, 7]])
    td.plot([1, 0, 3], [0, 1, 2])
    td.scatter([[1, 1, 1]])
    plt.show()
