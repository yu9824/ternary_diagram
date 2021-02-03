import PySimpleGUI as sg
import pandas as pd
import numpy as np
import xlrd
from copy import deepcopy
import matplotlib.pyplot as plt
from copy import copy

# matplotlibを埋め込むときに必要
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 自作モジュール
from ternary_diagram import ternary_diagram
from element_recognition import element_recognition, make_compositions, get_ratio


# ****** 変数定義 *********
font_family = 'Helvetica'
font_size = '20'

# options
options_font = {
    'font': (font_family, font_size),
}

options_popup = {
    'modal': False,
    # 'keep_on_top': True,
}
options_popup.update(options_font)

options_img_button = {
    'image_size':(2, 2),
    'image_subsample' : 5
}

# 初期値系
example = ['Li2O', 'La2O3', 'TiO2']

# path関係
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
default_path = os.path.join(os.getenv('HOME'), 'Desktop')

# windowを扱いやすいようにクラスを定義
class WindowBunch:
    def __init__(self, title = '', layout = ((sg.Text('You have to set something.')))):
        self.title = title
        self.layout = deepcopy(layout)  # itemを再生成したときに怒られるため．

        self.window = sg.Window(self.title, self.layout, **options_font, resizable = True, element_justification = 'center')
        self.window.Finalize()
    
    def read(self):
        self.event, self.values = self.window.read()

    def __del__(self):
        self.window.close()


# グラフを扱うために必要な関数．
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side = 'top', fill = 'both', expand = 1)
    return figure_canvas_agg

# ファイルを読み込むときの関数
def read_file(f):
    if '.csv' in f:
        return pd.read_csv(f, header=None)
    elif '.xls' in f:
        return pd.read_excel(f, sheet_name = 0, header=None)
    else:
        raise NotImplementedError

# 分数やその他数字を小数に変換する
def convert2float(s):
    if s.count('/') > 1:
        raise ValueError
    elif '/' in s:
        return float(s.split('/')[0]) / float(s.split('/')[1])
    else:
        return float(s)

# テーマの指定
sg.theme('Dark Black')

def gui():
    # topの中のlayout
    layout_w_o_z = [
        [sg.Button('', key = 'w/o_z', image_filename = os.path.join(DIR_PATH, 'img/w_o_z.png'), **options_img_button)],
        [sg.Text('without "z"')],
    ]
    layout_w_z = [
        [sg.Button('', key = 'w/_z', image_filename = os.path.join(DIR_PATH, 'img/w_z.png'), **options_img_button)],
        [sg.Text('with "z"')],
    ]

    top = WindowBunch(title = 'start menu', layout = [
        [sg.Text('reactant{}'.format(i+1), size = (7, 1), justification='center'), sg.InputText(example[i], key = 'reactant{}'.format(i+1), size = (15, 1), justification='center')]
    for i, ex in enumerate(example)] + [
        [sg.Text('')],
        [sg.Text('Which mode?')],
        [sg.Frame('', layout_w_o_z, element_justification = 'center'), sg.Frame('', layout_w_z, element_justification = 'center')]
    ])


    while True:
        top.read()

        if top.event is None:
            break
        elif top.event in ('w/o_z', 'w/_z'):
            materials = [top.values['reactant' + str(i)] for i in range(1, 4)]
            df_data = pd.DataFrame()    # Add されたdataを格納しておくDataFrame

            # layout
            tbl_columns = ['composition'] + materials
            layout_ratio = [
                            [sg.Text(top.values['reactant{}'.format(i+1)], size = (10, 1), justification = 'center'), sg.InputText('1', key = materials[i], do_not_clear = False, size = (7, 1), justification = 'right')]
                            for i in range(3)] + [
                            [sg.Submit(button_text = 'Add', key = 'Add_R')],
                            [sg.Text('–' * 40)],
                            [sg.Text('File Import'), sg.Text('(.xlsx .xls .csv / No header)')],
                            [sg.FilesBrowse('Browse', file_types = (('CSV', '*.csv'), ('Excel file', '*.xlsx'), ('Excel file', '*.xls')), key = 'fnames_R', **options_font), sg.Button('Read', key = 'Read_R')],
                            ]
            layout_composition = [
                                    [sg.Text('e.g.) ' + make_compositions(materials, ratio = [1, 1, 1]).index[0], justification='center')],
                                    [sg.InputText(make_compositions(materials, ratio = [1, 1, 1]).index[0], key='composition', size = (17, 1), justification='center')],
                                    [sg.Text('')],
                                    [sg.Submit(button_text = 'Add', key = 'Add_C')],
                                    [sg.Text('–' * 40)],
                                    [sg.Text('File Import'), sg.Text('(.xlsx .xls .csv / No header)')],
                                    [sg.FilesBrowse('Browse', file_types = (('CSV','*.csv'), ('Excel file','*.xlsx'), ('Excel file','*.xls')), key = 'fnames_C', **options_font), sg.Button('Read', key = 'Read_C')],
                                    ]

            # layoutを作る際，モードによって異なる部分．
            if top.event == 'w/_z':
                layout_ratio.insert(3, [sg.Text('z', size = (10, 1), justification='center'), sg.InputText('0', key='z_R', size = (7, 1), do_not_clear = False, justification='right')])
                layout_composition.insert(2, [sg.Text('z', size = (3, 1), justification='center'), sg.InputText('0', key='z_C', size = (14, 1), do_not_clear = False, justification='right')])
                tbl_columns += ['z']

                def get_radio(key, default):
                    rd_options = {'size':(10, 1), 'group_id':'mode'}
                    return sg.Radio(key, default = default, key = key, **rd_options)

                layout_options = [
                        [sg.Text('min', size = (7, 1), justification='center'), sg.InputText('None', key = 'minimum', size = (7, 1), justification='right'), sg.Text('max', size = (7, 1), justification='center'), sg.InputText('None', key = 'maximum', size = (7, 1), justification='right')],
                        [get_radio('scatter', True), get_radio('contour', False)]
                    ]
            elif top.event == 'w/o_z':
                tbl_columns += ['color']

                layout_options = [
                        [sg.Text('Color', size = (20, 1), justification='center'), sg.InputText('auto1', key = '-COLOR-', size = (10, 1), justification='right')],
                        [sg.Text('e.g.) "auto" + integer, #00ff00 (color code), 0 (integer), (0, 256, 0, 1.0) (RGBA), black (string) etc.', size = (80, 1), justification='center')]
                    ]

            # メイン画面
            main = WindowBunch(title = 'ternary_diagram', layout = [
                                    [sg.Table([[None for _ in range(len(tbl_columns))]], headings = tbl_columns, key = '-TABLE-', display_row_numbers = True, auto_size_columns = False)],
                                    [sg.Frame('Ratio', layout_ratio, element_justification = 'center'), sg.Frame('Composition', layout_composition, element_justification = 'center')],
                                    # [sg.TabGroup([[sg.Tab('Ratio', layout_ratio, element_justification = 'center'), sg.Tab('Composition', layout_composition, element_justification = 'center')]])],
                                    [sg.Submit(button_text = 'Plot'), sg.Submit(button_text = 'Clear')],
                                    [sg.Frame('Options', layout_options, element_justification = 'center')]
                                ]
                            )

            while True:
                main.read()
                if main.event is None:
                    break
                elif 'Add' in main.event:
                    # 割合手入力の場合
                    if main.event == 'Add_R':
                        dict_ratio = {}
                        try:
                            # 入力された割合の値を小数に変換しつつ，辞書に保存
                            for k in materials:
                                v = main.values[k]
                                dict_ratio[k] = convert2float(v)
                        except ValueError:
                            sg.popup_error('You have not entered any. Or the value you entered is not good.\nCorrect: 1/3, 1, 1.0, 3.141 etc.', **options_popup)
                            continue
                        
                        dict_temp = {'composition': make_compositions(materials = materials, ratio = list(dict_ratio.values())).index[0]}
                        dict_temp.update(dict_ratio)
                        
                        if top.event == 'w/o_z':
                            dict_temp['color'] = main.values['-COLOR-']

                        # sortしつつDataFrameに．(z以外)
                        df_add = pd.DataFrame.from_dict({col: [dict_temp[col]] for col in tbl_columns if col != 'z'}, orient = 'columns')
                    elif main.event == 'Add_C':
                        df_add = get_ratio(products = main.values['composition'], materials = materials)
                        df_add.reset_index(inplace = True)
                        if top.event == 'w/o_z':
                            df_add = pd.concat([df_add, pd.Series(main.values['-COLOR-'], name = 'color')], axis = 1)
                        df_add.columns = [col for col in tbl_columns if col != 'z']

                    if top.event == 'w/_z':
                        try:
                            df_add = pd.concat([df_add, pd.Series([convert2float(main.values['z' + main.event[-2:]])], name = 'z')], axis = 1)  # main.event[-2:]の部分は_Rなのか_Cなのかを表している．
                        except ValueError:
                            sg.PopupError('You have to enter integer or float.', **options_popup)
                            continue

                    df_data = pd.concat([df_data, df_add], axis = 0, ignore_index = True, sort = False)
                elif 'Read' in main.event:
                    fnames = main.values['fnames_R'] if main.event == 'Read_R' else main.values['fnames_C']
                    if fnames == '':  # filesbrowseする前にReadボタンを押されてしまったら
                        sg.PopupError('You have to select the file before Read.', **options_popup)
                        continue

                    for f in fnames.split(';'):
                        if main.event == 'Read_R':
                            df_add = read_file(f)
                            df_add = pd.concat([pd.Series(make_compositions(materials = materials, ratio = df_add.iloc[:, 0:3].to_numpy()).index), df_add], axis = 1)
                            if top.event == 'w/o_z':
                                df_add = pd.concat([df_add, pd.Series([main.values['-COLOR-'] for _ in range(df_add.shape[0])], name = 'color')], axis = 1)
                            df_add.columns = tbl_columns
                            
                        elif main.event == 'Read_C':
                            df_memo = read_file(f)
                            df_add = get_ratio(products = df_memo.iloc[:, 0].to_numpy(), materials = materials)
                            df_add.reset_index(inplace = True)
                            df_add = pd.concat([df_add, pd.Series([main.values['-COLOR-']] * df_add.shape[0], name = 'color')], axis = 1)
                            df_add.columns = [tbl_columns[0] if i == 0 else col for i, col in enumerate(df_add.columns)]
                            if top.event == 'w/_z':
                                col_memo = copy(list(df_add.columns))
                                df_add = pd.concat([df_add, df_memo.iloc[:, 1]], axis = 1)
                                df_add.columns = col_memo + ['z']
                        df_data = pd.concat([df_data, df_add], axis = 0, ignore_index = True, sort = False)

                elif main.event == 'Plot':
                    if len(df_data) == 0:
                        sg.PopupError('There is no data added. Please push Add if you want to add data.', **options_popup)
                        continue
                    else:
                        # gridだけの図作成
                        td = ternary_diagram(materials)
                        td.ax.set_xlim([-0.05, 1.05])
                        td.ax.set_ylim([-0.05, 1.05])

                        # データが選択されたときの挙動
                        def event_picked(event):
                            x, y = event.mouseevent.xdata, event.mouseevent.ydata
                            distance_euc = np.linalg.norm(np.hstack([np.hstack(td.x['scatter']).reshape(-1, 1), np.hstack(td.y['scatter']).reshape(-1, 1)]) - np.array([x, y]), axis = 1)
                            i_min = np.argmin(distance_euc)
                            sg.PopupOK(df_data.loc[i_min, 'composition'], **options_popup)

                        # define the window layout
                        figpage = WindowBunch(title = 'check figure', layout = [
                                [sg.Text('Plot test')],
                                [sg.Canvas(key='-CANVAS-')],
                                [sg.Cancel(), sg.Button('Save')],
                                [sg.Checkbox('transparent', key = '-TRANSPARENT-')]
                            ])

                        # add the plot to the window
                        fig_canvas_agg = draw_figure(figpage.window['-CANVAS-'].TKCanvas, td.fig)

                        if 'z' in df_data.columns:
                            td_options = {'z':df_data.loc[:, 'z']}
                            try:
                                td_options['maximum'] = None if main.values['maximum'] == 'None' else convert2float(main.values['maximum'])
                                td_options['minimum'] = None if main.values['minimum'] == 'None' else convert2float(main.values['minimum'])
                            except ValueError:
                                sg.popup_error('You have to enter integer or float or None in "maximum" and "minimum".', **options_popup)
                                continue
                            if main.values['scatter']:
                                td.scatter(df_data.loc[:, materials], **td_options, picker = True)
                            elif main.values['contour']:
                                td.contour(df_data.loc[:, materials], **td_options)
                        else:
                            st_color = set(df_data.loc[:, 'color'])
                            for c in st_color:
                                if 'auto' in c:
                                    td_options = {}
                                else:
                                    td_options = {'color' : c}
                                td.scatter(df_data.loc[df_data.loc[:, 'color'] == c, materials], **td_options, picker = True)
                        
                        plt.tight_layout()

                        # コマンド
                        td.fig.canvas.mpl_connect('pick_event', event_picked)

                        while True:
                            figpage.read()
                            if figpage.event in ('Cancel', None):
                                break
                            elif figpage.event == 'Save':
                                fname = sg.popup_get_file('', save_as = True, default_path = default_path, file_types = (('PDF Format','*.pdf'), ('PNG','*.png'),), **options_font, modal = False)
                                if fname is not None:
                                    transparent = figpage.values['-TRANSPARENT-']
                                    td.fig.savefig(fname, dpi = 300, transparent = transparent)
                                    sg.PopupOK('Saved successfully.', **options_popup)
                        plt.close()
                        del td
                        del figpage
                elif main.event == 'Clear':
                    df_data = pd.DataFrame()    # Add されたdataを格納しておくDataFrameを初期化
                else:
                    sg.PopupError('Something Wrong', **options_popup)
                main.window['-TABLE-'].update(values = df_data.to_numpy().tolist())
            del main
    del top

if __name__ == '__main__':
    gui()