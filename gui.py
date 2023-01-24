import PySimpleGUI as sg
import pandas as pd
import numpy as np
from fuzzy_topsis.main import fuzzy_topsis_do_gui
from RSM.RSM import RSM
# from SPCP import SPCP
from UTA.main import uta
from input_validation import validate
from ranking_comparision.compare import Spearman_s_Footrule

_VARS = {
    'window': False,
    'fig_agg': False,
    'pltFig': False
}

#TODO dodac nazwy funkcji
algos = {
    'FUZZY_TOPSIS': fuzzy_topsis_do_gui,
    'RSM': RSM,
    'SAFETY_PRINCIPAL': '???',
    'UTA': uta
}

list_k = [
    'Miasto', 
    'Nazwa kierunku', 
    'Nazwa uczelni',
    'Procent zdawalności', 
    'Ocena absolwentów',
    'Własna ocena sylabusa', 
    'Ilość semestrów',
    'Próg rekrutacji', 
    'Rodzaj kierunku'
]
result_headings = [
    'Nazwa kierunku',
    'Nazwa uczelni',
    'Miasto',
    'Score'
]
types = {
    'Wszystkie': 'SWD_DB',
    'Techniczne': 'tech',
    'Humanistyczne': 'hum',
    'Ekonomiczne': 'ekon',
    'Lekarskie': 'lek',
    'Ścisłe': 'sci',
    'Społeczne': 'spo',
    'Sportowe': 'sport',
    'Wojskowe':'wojs'
}

weights_layout = [
    [sg.Text('Podaj wagi (0 - 1)', justification='center')],
    [sg.InputText(key=f'-WEIGHT{str(i)}-', size=(22, 1), default_text='0.00') for i in range(len(list_k[3: -1]))],
    [sg.Text('')]
]

criteria_layout = [
    [sg.Text('Podaj kryteria (min/max)', justification='center')],
    [sg.Text(list_k[i], size=(20, 1)) for i in range(len(list_k[3: -1]))],
    [sg.Combo(values=['min', 'max'], default_value='min', key=f'-CRIT{str(i)}-', size=(20, 1)) for i in range(len(list_k[3: -1]))],
    [sg.Text('')]
]

choose_type_layout = [
    [sg.Text('Wybierz rodzaj kierunku'), sg.Combo(key='-TYPE-', values=list(types.keys()), default_value=list(types.keys())[0], size=(50, 10))],
    [sg.Text('')]
]

choose_algo_layout = [
    [sg.Text('Wybierz algorytm'), sg.Combo(key='-ALGO-', values=list(algos.keys()), default_value=list(algos.keys())[0], size=(50, 10))],
    [sg.Text('')]
]

create_rank_layout = [
    [sg.Button('Stwórz ranking',key='-BUTTON_RANKING-')]
]

alternatives_layout = [
    [sg.Text('Alternatywy z kryteriami', justification='center')],
    [sg.Table([], headings=list_k,key='-TABLE_KRYT-', num_rows=10, max_col_width = 5, auto_size_columns=True, vertical_scroll_only=False, justification='center', expand_x=True, expand_y=True)]
]

# class_layout = [
#     [sg.Text('Klasy',justification='center')],
#     [sg.Table([], ['Punkt','Klasa'], key='-TABLE_CLASS-', num_rows=10)]
# ]

disp_ranking_layout = [
    [sg.Text('Ranking',justification='center')],
    [sg.Table([], result_headings, key='-TABLE_RANK-', num_rows=10, auto_size_columns=True)]
]

compare_layout = [
    [sg.Text('Wybierz algorytmy do porównania')],
    [sg.Combo(key='-ALGO1-', values=list(algos.keys()), default_value=list(algos.keys())[0], size=(10, 1)), sg.Combo(key='-ALGO2-', values=list(algos.keys()), default_value=list(algos.keys())[0], size=(10, 1))],
    [sg.Text('')],
    [sg.Button('Porównaj rankingi',key='-COMPARE_RANKING-')]
]

disp_comparision_layout = [
    [sg.Text('', justification='center', key='-OUT-')]
]

layout = [
    [choose_type_layout],
    [criteria_layout],
    [weights_layout],
    [choose_algo_layout],
    [create_rank_layout],
    [sg.Col(alternatives_layout,vertical_alignment='top')],
    [disp_ranking_layout],
    [compare_layout],
    [disp_comparision_layout]
]

_VARS['window'] = sg.Window('GUI_UwU',
                            layout,
                            finalize=True,
                            resizable=True,
                            size=(1000,800),
                            element_justification='center')

def read_add_params() -> dict:
    
    weights = np.array([values[f'-WEIGHT{i}-'] for i in range(len(list_k[3: -1]))])
    criteria = np.array([values[f'-CRIT{i}-'] for i in range(len(list_k[3: -1]))])
    
    regex = "^[+-]?([0](\.(\d{0,2}))?)?$"
    
    if validate(weights, regex):
        
        weights = [float(i) for i in weights]
        additional_params = {
                    'FUZZY_TOPSIS': (weights, criteria), #checked
                    'RSM': criteria, #checked
                    'SAFETY_PRINCIPAL': ['???'],
                    'UTA': criteria #checked
                }
        
        return additional_params, weights, criteria
    
    else:
        sg.popup('Wprowadzone dane są niepoprawne\nSpróbuj ponownie')
        pass


while True:
    
    event, values = _VARS['window'].read(timeout=200)
    
    if event == sg.WIN_CLOSED:
        break
    
    # Obliczenie rankingu pojedyńczą metodą
    if event == '-BUTTON_RANKING-':
        
        # weights = np.array([values[f'-WEIGHT{i}-'] for i in range(len(list_k[3: -2]))])
        # criteria = np.array([values[f'-CRIT{i}-'] for i in range(len(list_k[3: -2]))])
        additional_params, weights, criteria = read_add_params()
       
        # Load database
        db = pd.read_csv(f"./datasets/{types[values['-TYPE-']]}.csv", sep=',')
        _VARS['window']['-TABLE_KRYT-'].update(values=list(map(tuple, db.values)))
        
        # Call algorithm if not called before
        if f"{values['-ALGO-']}_score" not in db.columns:
            db = algos[values['-ALGO-']](db, additional_params[values['-ALGO-']])

        _VARS['window']['-TABLE_RANK-'].update(values=list(map(tuple, db.sort_values(by=[f"{values['-ALGO-']}_score"], ascending=False)[result_headings[:-1] + [f"{values['-ALGO-']}_score"]].values)))
        
            
    # Porównanie rankingów
    if event == '-COMPARE_RANKING-':
        
        # weights = np.array([values[f'-WEIGHT{i}-'] for i in range(len(list_k[3: -2]))])
        # criteria = np.array([values[f'-CRIT{i}-'] for i in range(len(list_k[3: -2]))])
        
        additional_params, weights, criteria = read_add_params()
            
        db = pd.read_csv(f"./datasets/{types[values['-TYPE-']]}.csv", sep=',')
        _VARS['window']['-TABLE_KRYT-'].update(values=list(map(tuple, db.values)))
    
        if f"{values['-ALGO1-']}_score" not in db.columns:
            db = algos[values['-ALGO1-']](db, additional_params[values['-ALGO1-']])

        if f"{values['-ALGO2-']}_score" not in db.columns:
            db = algos[values['-ALGO2-']](db, additional_params[values['-ALGO2-']])
            
        rank_1 = [idx for idx in db.sort_values(by=[f"{values['-ALGO1-']}_score"], ascending=False).index]
        rank_2 = [idx for idx in db.sort_values(by=[f"{values['-ALGO2-']}_score"], ascending=False).index]
        compare_result = Spearman_s_Footrule(rank_1, rank_2)
        _VARS['window']['-OUT-'].update(value=str(compare_result))
        print(compare_result)
        
_VARS['window'].close()