import PySimpleGUI as sg
import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as plt
from copy import copy

# matplotlibを埋め込むときに必要
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 自作モジュール
from ternary_diagram import ternary_diagram
from element_recognition import *

window_options = {}
window_options['font'] = 'Helvetica 18'

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# sg.theme_previewer()

default_path = os.path.join(os.getenv('HOME'), 'Desktop')


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side = 'top', fill = 'both', expand = 1)
    return figure_canvas_agg

def read_window(d):
    d['event'], d['values'] = d['window'].read()

def read_file(f):
    if '.csv' in f:
        return pd.read_csv(f, header=None)
    elif '.xls' in f:
        return pd.read_excel(f, sheet_name = 0, header=None)



sg.theme('Dark Black')

example = ['Li2O', 'LaO3', 'TiO2']
top = {}
top_button_options = {'image_size':(2, 2), 'image_subsample' : 3}

layout_w_o_z = [
    [sg.Button('', key = 'w/o_z', image_filename = os.path.join(DIR_PATH, 'img/w_o_z.png'), **top_button_options)],
    [sg.Text('without "z"')],
]
layout_w_z = [
    [sg.Button('', key = 'w/_z', image_filename = os.path.join(DIR_PATH, 'img/w_z.png'), **top_button_options)],
    [sg.Text('with "z"')],
]

top['layout'] = [
    [sg.Text('reactant ' + str(i+1), size = (7, 1), justification='center'), sg.InputText(example[i], key = 'reactant' + str(i+1), size = (15, 1), justification='center')]
for i, ex in enumerate(example)] + [
    [sg.Text('')],
    [sg.Text('Which mode?')],
    [sg.Frame('', layout_w_o_z, element_justification = 'center'), sg.Frame('', layout_w_z, element_justification = 'center')]
]


top['window'] = sg.Window('ternary_diagram', top['layout'], **window_options, element_justification = 'center')

while True:
    read_window(top)
    # top['event'], top['values'] = top['window'].read()

    if top['event'] is None:
        break


    if top['event'] in ('w/o_z', 'w/_z'):
        materials = [top['values']['reactant' + str(i)] for i in range(1, 4)]
        manual_add = {}
        df_data = pd.DataFrame()    # Add されたdataを格納しておくDataFrame

        # layout
        tbl_columns = ['composition'] + materials
        layout_ratio = [
                        [sg.Text(top['values']['reactant' + str(i)], size = (10, 1), justification='center'), sg.InputText('1', key='ratio' + str(i), do_not_clear = False, size = (7, 1), justification='right')]
                        for i in range(1,4)] + [
                        [sg.Submit(button_text = 'Add', key = 'Add_R')],
                        [sg.Text('–' * 40)],
                        [sg.Text('File Import'), sg.Text('(.xlsx .xls .csv / No header)')],
                        [sg.FilesBrowse('Browse', file_types = (('CSV', '*.csv'), ('Excel file', '*.xlsx'), ('Excel file', '*.xls')), key = 'fnames_R', **window_options), sg.Button('Read', key = 'Read_R')],
                        ]
        layout_composition = [
                                [sg.Text('e.g.) ' + MakeComposition(materials, ratio = [1, 1, 1]).index[0], justification='center')],
                                [sg.InputText(MakeComposition(materials, ratio = [1, 1, 1]).index[0], key='composition', size = (17, 1), justification='center')],
                                [sg.Text('')],
                                [sg.Submit(button_text = 'Add', key = 'Add_C')],
                                [sg.Text('–' * 40)],
                                [sg.Text('File Import'), sg.Text('(.xlsx .xls .csv / No header)')],
                                [sg.FilesBrowse('Browse', file_types = (('CSV','*.csv'), ('Excel file','*.xlsx'), ('Excel file','*.xls')), key = 'fnames_C', **window_options), sg.Button('Read', key = 'Read_C')],
                                ]

        if top['event'] == 'w/_z':
            layout_ratio.insert(3, [sg.Text('z', size = (10, 1), justification='center'), sg.InputText('0', key='z_R', size = (7, 1), do_not_clear = False, justification='right')])
            layout_composition.insert(2, [sg.Text('z', size = (3, 1), justification='center'), sg.InputText('0', key='z_C', size = (14, 1), do_not_clear = False, justification='right')])
            tbl_columns += ['z']
        elif top['event'] == 'w/o_z':
            tbl_columns += ['color']

        manual_add['layout'] = [
                                [sg.Table([[None for _ in range(len(tbl_columns))]], headings = tbl_columns, key = '-TABLE-', display_row_numbers = True, auto_size_columns = False)],
                                [sg.Frame('Ratio', layout_ratio, element_justification = 'center'), sg.Frame('Composition', layout_composition, element_justification = 'center')],
                                # [sg.TabGroup([[sg.Tab('Ratio', layout_ratio, element_justification = 'center'), sg.Tab('Composition', layout_composition, element_justification = 'center')]])],
                                [sg.Submit(button_text = 'Plot'), sg.Submit(button_text = 'Clear')]
                                ]
        if top['event'] == 'w/_z':
            def get_radio(key, default):
                rd_options = {'size':(10, 1), 'group_id':'mode'}
                return sg.Radio(key, default = default, key = key, **rd_options)

            layout_options = [
                    [sg.Text('min', size = (7, 1), justification='center'), sg.InputText(None, key = 'minimum', size = (7, 1), justification='right'), sg.Text('max', size = (7, 1), justification='center'), sg.InputText(None, key = 'maximum', size = (7, 1), justification='right')],
                    [get_radio('scatter', True), get_radio('contour', False)]
                ]
        elif top['event'] == 'w/o_z':
            layout_options = [
                    [sg.Text('Color', size = (20, 1), justification='center'), sg.InputText('auto1', key = '-COLOR-', size = (10, 1), justification='right')],
                    [sg.Text('e.g.) "auto" + integer, #00ff00 (color code), 0 (integer), (0, 256, 0, 1.0) (RGBA), black (string) etc.', size = (80, 1), justification='center')]
                ]
        manual_add['layout'].insert(-1, [sg.Frame('Options', layout_options, element_justification = 'center')])

        # manual_add['layout'] = [[sg.Text(top['values']['reactant' + str(i)], size=(15, 1)), sg.InputText('', key='ratio' + str(i), do_not_clear = False, size = (7, 1))] for i in range(1,4)] + [[sg.Submit(button_text = 'Add'), sg.Submit(button_text = 'Plot'), sg.Submit(button_text = 'Clear')]]

        manual_add['window'] = sg.Window('ternary_diagram', manual_add['layout'], element_justification = 'center', **window_options)
        while True:
            read_window(manual_add)
            if manual_add['event'] is None:
                break
            elif 'Add' in manual_add['event']:
                if manual_add['event'] == 'Add_R':
                    input_ratio = [manual_add['values']['ratio' + str(i)]for i in range(1, 4)]
                    try:
                        df_add = pd.DataFrame(map(float, [manual_add['values']['ratio' + str(i)]for i in range(1, 4)])).T
                    except ValueError:
                        sg.popup('You have to enter integer or float.', **window_options)
                        continue
                    else:
                        df_add = pd.concat([pd.Series(MakeComposition(materials = materials, ratio = df_add.to_numpy()).index), df_add], axis = 1)
                        if top['event'] == 'w/o_z':
                            df_add = pd.concat([df_add, pd.Series(manual_add['values']['-COLOR-'], name = 'color')], axis = 1)
                        df_add.columns = tbl_columns[:df_add.shape[1]]
                elif manual_add['event'] == 'Add_C':
                    df_add = Ratio(products = manual_add['values']['composition'], materials = materials)
                    df_add.reset_index(inplace = True)
                    if top['event'] == 'w/o_z':
                            df_add = pd.concat([df_add, pd.Series(manual_add['values']['-COLOR-'], name = 'color')], axis = 1)
                    df_add.columns = [tbl_columns[0] if i == 0 else col for i, col in enumerate(df_add.columns)]

                if top['event'] == 'w/_z':
                    try:
                        df_add = pd.concat([df_add, pd.Series([float(manual_add['values']['z' + manual_add['event'][-2:]])], name = 'z')], axis = 1)
                    except ValueError:
                        sg.popup('You have to enter integer or float.', **window_options)
                        continue

                df_data = pd.concat([df_data, df_add], axis = 0, ignore_index = True, sort = False)
            elif 'Read' in manual_add['event']:
                fnames = manual_add['values']['fnames_R'] if manual_add['event'] == 'Read_R' else manual_add['values']['fnames_C']
                if fnames == '':  # filesbrowseする前にReadボタンを押されてしまったら
                    continue

                for f in fnames.split(';'):
                    if manual_add['event'] == 'Read_R':
                        df_add = read_file(f)
                        df_add = pd.concat([pd.Series(MakeComposition(materials = materials, ratio = df_add.iloc[:, 0:3].to_numpy()).index), df_add], axis = 1)
                        if top['event'] == 'w/o_z':
                            df_add = pd.concat([df_add, pd.Series([manual_add['values']['-COLOR-'] for _ in range(df_add.shape[0])], name = 'color')], axis = 1)
                        df_add.columns = tbl_columns
                        
                    elif manual_add['event'] == 'Read_C':
                        df_memo = read_file(f)
                        df_add = Ratio(products = df_memo.iloc[:, 0].to_numpy(), materials = materials)
                        df_add.reset_index(inplace = True)
                        df_add = pd.concat([df_add, pd.Series([manual_add['values']['-COLOR-']] * df_add.shape[0], name = 'color')], axis = 1)
                        df_add.columns = [tbl_columns[0] if i == 0 else col for i, col in enumerate(df_add.columns)]
                        if top['event'] == 'w/_z':
                            col_memo = copy(list(df_add.columns))
                            df_add = pd.concat([df_add, df_memo.iloc[:, 1]], axis = 1)
                            df_add.columns = col_memo + ['z']
                    df_data = pd.concat([df_data, df_add], axis = 0, ignore_index = True, sort = False)

            elif manual_add['event'] == 'Plot':
                if len(df_data) == 0:
                    sg.popup_error('There is no data added. Please push Add if you want to add data.', **window_options)
                    continue
                else:
                    # gridだけの図作成
                    td = ternary_diagram(df_data.columns[1:4])
                    if 'z' in df_data.columns:
                        td_options = {'z':df_data.loc[:, 'z']}
                        try:
                            td_options['maximum'] = None if manual_add['values']['maximum'] == 'None' else float(manual_add['values']['maximum'])
                            td_options['minimum'] = None if manual_add['values']['minimum'] == 'None' else float(manual_add['values']['minimum'])
                        except ValueError:
                            sg.popup_error('You have to enter integer or float or None in "maximum" and "minimum".', **window_options)
                            continue
                        if manual_add['values']['scatter']:
                            td.scatter(df_data.iloc[:, 1:4], **td_options)
                        elif manual_add['values']['contour']:
                            td.contour(df_data.iloc[:, 1:4], **td_options)
                    else:
                        st_color = set(df_data.loc[:, 'color'])
                        for c in st_color:
                            if 'auto' in c:
                                td_options = {}
                            else:
                                td_options = {'color' : c}
                            td.scatter(df_data.loc[df_data.loc[:, 'color'] == c].iloc[:, 1:4], **td_options)
                        
                    

                    # define the window layout
                    figpage = {}
                    figpage['layout'] = [
                            [sg.Text('Plot test')],
                            [sg.Canvas(key='-CANVAS-')],
                            [sg.OK(), sg.Submit('Save')],
                            [sg.Checkbox('transparent', key = '-TRANSPARENT-')]
                        ]

                    # create the form and show it without the plot
                    figpage['window'] = sg.Window('Check figure', figpage['layout'], finalize=True, element_justification='center', **window_options)

                    # add the plot to the window
                    fig_canvas_agg = draw_figure(figpage['window']['-CANVAS-'].TKCanvas, td.fig)

                    while True:
                        read_window(figpage)
                        if figpage['event'] == 'Save':
                            fname = sg.popup_get_file('', save_as=True, default_path = default_path, file_types = (('PDF Format','*.pdf'), ('PNG','*.png'),), **window_options)
                            if fname is not None:
                                transparent = figpage['values']['-TRANSPARENT-']
                                td.fig.savefig(fname, dpi = 300, transparent = transparent)
                            else:
                                continue
                        elif figpage['event']in (None, 'OK'):
                            break
                        else:
                            print(figpage['event'])
                    figpage['window'].close()
            elif manual_add['event'] == 'Clear':
                df_data = pd.DataFrame()    # Add されたdataを格納しておくDataFrameを初期化
            else:
                sg.popup_error('Something Wrong')
            manual_add['window']['-TABLE-'].update(values = df_data.to_numpy().tolist())
        manual_add['window'].close()

top['window'].close()
