import numpy as np
import pandas as pd

from copy import deepcopy

import matplotlib.pyplot as plt
import matplotlib.cm as cm      # ternary内にカラーマップを創設する
import matplotlib.tri as tri    # 三角図を簡単に出すやつ

'''
    options
maximum: colorbarの上限値を固定するかどうか．default;None
minimum: colorbarの上限値を固定するかどうか．default;None
norm: 標準化する必要があるかどうか．default;True
bar_label: colorbarの横に書くlabel名
'''

__all__ = [
    'TernaryDiagram',
]

class TernaryDiagram:
    def __init__(self, materials, fontfamily = 'Helvetica'):
        '''
        Make instance.

        Parameters
        ----------
        materials : list
            A one-dimensional list of compounds that constitute an endpoint when generating a ternary_diagram.
        '''
        plt.rcParams['font.family'] = fontfamily

        # 単色scatterのときにcolormapのうち何番目までを使ったかを保存しておく変数とcolormapの指定
        self.color_counta = 0
        self.mono_cmap = plt.get_cmap('Set1')

        # figure, axisオブジェクトの生成
        self.fig = plt.figure(facecolor='white')    # jupyter note / lab だと背景が透過色になっていて，保存すると変な感じになるため．もし背景透過で保存したい場合はfig.savefig('filename', transparent = True)とする．
        self.ax = self.fig.add_subplot(111)

        # material_labelを生成
        material_label = list(map(self._get_label, materials))

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
        self.ax.text(0.5, h+0.02, material_label[0], fontsize=16, ha = 'center', va = 'bottom')
        self.ax.text(0, -0.05, material_label[1], fontsize=16, ha = 'right', va = 'top')#, rotation=300)
        self.ax.text(1, -0.05, material_label[2], fontsize=16, ha = 'left', va = 'top')#, rotation=60)

        #軸ラベル
        for i in range(1,10):
            self.ax.text(0.5+(10-i)/20.0, h*(1.0-(10-i)/10.0), '%d0' % i, fontsize = 10)
            self.ax.text((10-i)/20.0-0.06, h*(10-i)/10.0+0.02, '%d0' % i, fontsize = 10, rotation = 300)
            self.ax.text(i/10.0-0.03, -0.07, '%d0' % i, fontsize = 10, rotation = 60)

        # 二次元に変換したデータを保存しておく
        self.x = {
            'scatter': [],
            'contour': [],
            'plot': [],
        } 
        self.y = deepcopy(self.x)

    # *** サブ関数 ***
    def _get_from_options(self, options, key, default):
        return options[key] if key in options else default

    def _three2two(self, vector):
        return (2 * vector[:, 2] + vector[:, 0]) / 2, np.sqrt(3) / 2 * vector[:, 0]
    
    def _get_label(self, name):
        if not isinstance(name, str):
            raise ValueError('The "name" must be string.')
        f = '$_{'
        b = '}$'
        N = len(name)
        lst_name = list(name) + ['']   # outputするために変えていく．

        # １文字ずつ取り出して
        i = 0
        while i < N:
            l = name[i] # l: letter
            if l.isdigit():
                j = i + 1
                while j < N + 1:
                    try:
                        float(name[i:j])
                    except ValueError:
                        break
                    else:
                        j += 1
                j -= 1
                lst_name[i] = f + lst_name[i]
                try:
                    lst_name[j] = b + lst_name[j]
                except:
                    print('aaa', j, N)
                # print(lst_name[i] = name[i:j])
                i = j
            i += 1
        return ''.join(lst_name)

    class _common:
        def __init__(self, outer, vector, **options):
            # クラスオブジェクト
            self.options = options

            # numpy.ndarray化
            self.vector = np.array(vector)

            # 正規化するかどうか．
            norm = self.options.pop('norm') if 'norm' in self.options else True
            if norm:
                # self.vectorの正規化
                self.vector = self.vector / np.sum(self.vector, axis = 1, keepdims = True) # 今回keepdims = Trueは.reshape(-1, 1)と同義

            # 3次元ベクトルをx, y座標に落とし込む．
            self.x, self.y = outer._three2two(self.vector)

            # 念のためself.zをnp.ndarrayにしてflatten
            self.z = np.array(self.options.pop('z')).flatten() if 'z' in self.options else None

            if self.z is not None:
                self.maximum = self.options.pop('maximum') if 'maximum' in self.options else None
                self.minimum = self.options.pop('minimum') if 'minimum' in self.options else None
                self.bl = self.options.pop('bar_label') if 'bar_label' in self.options else ''

        def colorbar(self):
            plt.colorbar(self.triplot, shrink = 0.8, format='%.1f', label = self.bl, orientation = 'vertical', ticklocation = 'top')


    class _scatter_(_common):
        def __init__(self, outer, vector, **options):   # なぜか**kwargsで継承クラスの初期化メソッドともども使うとダメだった．
            super().__init__(outer, vector, **options)   # TernaryDiagramクラスのselfを引数として与えている．

            self.name = 'scatter'
            outer.x[self.name].append(self.x)
            outer.y[self.name].append(self.y)

            # easy annotation 右上に簡易annotation
            self.annotations = self.options.pop('annotations') if 'annotations' in self.options else []
            for x, y, ann in zip(self.x, self.y, self.annotations):
                outer.ax.annotate(ann, xy = (x, y), xytext = (x+0.02, y+0.02), fontsize = 8, color = '#262626')

            # scatterにおいてzorderを指定してしまうと複数入力になってしまうため，それへの対処．
            zorder = self.options.pop('zorder') if 'zorder' in self.options else 2

            # zに値が指定されていないとき
            if self.z is None:
                # 色について (単色なのは zがNoneのときだけなので)
                if 'c' in self.options and 'color' in self.options:
                    raise ValueError("Supply a 'c' argument or a 'color' kwarg but not both")
                elif 'c' in self.options:
                    outer.color = self.options['c']
                elif 'color' in self.options:
                    outer.color = self.options['color']
                elif 'edgecolors' in self.options:
                    outer.color = self.options['edgecolors']

                if not('c' in self.options or 'color' in self.options or 'facecolor' in self.options or 'facecolors' in self.options):
                    self.options['color'] = outer.mono_cmap(outer.color_counta)    # 各点ごとに色を指定するのが普通っぽいので， 点の数分で二次元化
                    outer.color = self.options['color']
                    outer.color_counta += 1
                
                outer.ax.scatter(self.x, self.y, zorder = zorder, **self.options)
            else:
                if 'cmap' not in self.options:
                    self.options['cmap'] = 'rainbow'
                self.triplot = outer.ax.scatter(self.x, self.y, c = self.z, vmin = self.minimum, vmax = self.maximum, zorder = zorder, **self.options)
                self.colorbar()

    class _contour_(_common):
        def __init__(self, outer, vector, **options):   # なぜか**kwargsで継承クラスの初期化メソッドともども使うとダメだった．
            super().__init__(outer, vector, **options)   # TernaryDiagramクラスのselfを引数として与えている．

            self.name = 'contour'
            outer.x[self.name].append(self.x)
            outer.y[self.name].append(self.y)

            if 'cmap' not in self.options:
                self.options['cmap'] = 'rainbow'

            T = tri.Triangulation(self.x, self.y)
            self.triplot = outer.ax.tricontourf(self.x, self.y, T.triangles, self.z, np.linspace(self.minimum if self.minimum is not None else np.min(self.z), self.maximum if self.maximum is not None else np.max(self.z), 101), **self.options)
            self.colorbar()

    class _plot_(_common):
        def __init__(self, outer, vector, **options):
            super().__init__(outer, vector, **options)

            self.name = 'plot'
            outer.x[self.name].append(self.x)
            outer.y[self.name].append(self.y)

            if 'zorder' not in self.options:
                options['zorder'] = 1
            if not('color' in self.options or 'c' in self.options):
                self.options['color'] = outer.color

            #option系
            if not('linewidth' in self.options or 'lw' in self.options):
                self.options['lw'] = 1

            # plot
            outer.ax.plot(self.x, self.y, **self.options)

    def scatter(self, vector, **options):
        '''
        To plot scatter points.

        Parameters
        ----------
        vector : list, numpy.ndarray, pandas.DataFrame etc.
            percentage of each compound mixed in 2D list / pandas.DataFrame / numpy.ndarray, where shape = [n, 3] (n is the number of samples to be plotted as integer)
        
        annotations : list
        '''
        self._scatter_(self, vector, **options) # selfオブジェクトを渡してる．

    def contour(self, vector, **options):
        '''
        To create a contour map.

        Parameters
        ----------
        vector : list, numpy.ndarray, pandas.DataFrame etc.
            percentage of each compound mixed in 2D list / pandas.DataFrame / numpy.ndarray, where shape = [n, 3] (n is the number of samples to be plotted as integer)
        '''
        self._contour_(self, vector, **options) # selfオブジェクトを渡してる．

    def plot(self, r1, r2, **options):   # 連結線を引く (scatterオブジェクトの使用が必須な状況)
        '''
        To draw a tie line.

        Parameters
        ----------
        r1, r2 : list
            A mixing ratio of the compounds that are endpoints of the connecting line. A one-dimensional list of length 3.
        '''
        vector = np.array([r1, r2])
        self._plot_(self, vector, **options)



if __name__ == '__main__':
    df = pd.read_csv('example/scatter/example_scatter.csv')
    # fig = TernaryDiagram(df.columns[0:-1], df.iloc[:, 0:-1])
    # plt.show()

    td = TernaryDiagram(['Li2O', 'La2O3', 'TiO2'])

    # N = 1000
    # td.contour(np.random.rand(3 * N).reshape(N, 3), z = np.random.rand(N))
    # td.scatter([[6, 1, 3]], z = [1])
    td.scatter([[1, 2, 7]], zorder = 2)
    td.plot([1, 0, 3], [0, 1, 2])
    td.scatter([[1, 1, 1]])
    print(td.x, td.y)
    plt.show()
