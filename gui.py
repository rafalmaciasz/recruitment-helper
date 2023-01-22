import PySimpleGUI as sg
import pandas as pd
import numpy as np
from fuzzy_topsis.fuzzy_topsis import fuzzy_topsis
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
    'FUZZY TOPSIS': fuzzy_topsis,
    'RSM': RSM,
    'SAFETY PRINCIPAL': '???',
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
    [sg.InputText(key=f'-WEIGHT{str(i)}-', size=(5, 1), default_text='0.00') for i in range(len(list_k[3: -2]))],
    [sg.Text('')]
]

criteria_layout = [
    [sg.Text('Podaj kryteria (min/max)', justification='center')],
    [sg.Combo(values=['min', 'max'], default_value='min', key=f'-CRIT{str(i)}-', size=(5, 1)) for i in range(len(list_k[3: -2]))],
    [sg.Text('')]
]

weights = []
criteria = []

#TODO dodac paramsy funkcji
additional_params = {
    'FUZZY TOPSIS': [weights, criteria],
    'RSM': [], #checked
    'SAFETY PRINCIPAL': ['???'],
    'UTA': ['???']
}

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
    [sg.Text('Alternatywy z kryteriami',justification='center')],
    [sg.Table([], headings=list_k,key='-TABLE_KRYT-', max_col_width = 5, auto_size_columns=True, vertical_scroll_only=False, justification='center', expand_x=True, expand_y=True)]
]

class_layout = [
    [sg.Text('Klasy',justification='center')],
    [sg.Table([], ['Punkt','Klasa'], num_rows=2)]
]

compare_layout = [
    [sg.Text('Wybierz algorytmy do porównania')],
    [sg.Combo(key='-ALGO1-', values=list(algos.keys())[1:], default_value=list(algos.keys())[1], size=(10, 1)), sg.Combo(key='-ALGO2-', values=list(algos.keys())[1:], default_value=list(algos.keys())[1], size=(10, 1))],
    [sg.Text('')],
    [sg.Button('Porównaj rankingi',key='-COMPARE_RANKING-')]
]

disp_ranking_layout = [
    [sg.Text('Ranking',justification='center')],
    [sg.Table([], ['Nazwa kierunku','Wynik'], num_rows=2)]
]

layout = [
    [choose_type_layout],
    [criteria_layout],
    [weights_layout],
    [choose_algo_layout],
    [create_rank_layout],
    [sg.Col(class_layout,vertical_alignment='top'),sg.Col(alternatives_layout,vertical_alignment='top')],
    [compare_layout],
    [disp_ranking_layout]
]

_VARS['window'] = sg.Window('GUI_UwU',
                            layout,
                            finalize=True,
                            resizable=True,
                            size=(500,500),
                            element_justification='center')

while True:
    
    event, values = _VARS['window'].read(timeout=200)
    
    if event == sg.WIN_CLOSED:
        break
    
    # if event == '-BUTTON_INSERT-':
    #     with open(f"./datasets/{types[values['-TYPE-']]}.csv", 'r') as file:
    #         data = csv.reader(file)
    #         list_of_csv = list(map(tuple, data))
    #     print(len(list_of_csv))
    #     print(list_of_csv)
        
    #     if len(list_of_csv) != 0:
    #         sg.popup('Pobrano dane',line_width=40)
    #     else:
    #         sg.popup('Brak danych')
    
    #TODO wymyslec jak dodac inputy dla wag i min/max        
    # if event == '-ALGO-':
    #     _VARS['window'].add_rows(additional_params[values['-ALGO-']])
        # _VARS["window"].
    
    if event == '-BUTTON_RANKING-':
        
        # with open(f"./datasets/{types[values['-TYPE-']]}.csv", 'r') as file:
        #     data = csv.reader(file)
        #     list_of_csv = list(map(tuple, data))
        # print(len(list_of_csv))
        
        weights = np.array([values[f'-WEIGHT{i}-'] for i in range(len(list_k[3: -2]))])
        criteria = np.array([values[f'-CRIT{i}-'] for i in range(len(list_k[3: -2]))])
        
        regex = "^[+-]?([0](\.(\d{0,2}))?)?$"
        
        if validate(weights, regex):
            
            # Load database
            db = pd.read_csv(f"./datasets/{types[values['-TYPE-']]}.csv", sep=',')
            
            # Call algorithm if not called before
            if f"{values['-ALGO-']}_score" not in db.columns:
                db = algos[values['-ALGO-']](db, criteria)
                # pass
                
            
            _VARS['window']['-TABLE_KRYT-'].update(values=list(map(tuple, db.sort_values(by=[f"{values['-ALGO-']}_score"], ascending=False).values)))
            
        else:
            sg.popup('Wprowadzone dane są niepoprawne\nSpróbuj ponownie')
            
    # Porównanie rankingów
    if event == '-COMPARE_RANKING-':
        if f"{values['-ALGO1-']}_score" not in db.columns:
            # db = algos[values['-ALGO1-']](db, jakies_dodatkowe_gowno)
            pass
        if f"{values['-ALGO2-']}_score" not in db.columns:
            # db = algos[values['-ALGO2-']](db, jakies_dodatkowe_gowno)
            pass
        # rank_1 = [idx for idx in db.sorted_values(by=[f"{values['-ALGO1-']}_score"], ascending=False).index]
        # rank_2 = [idx for idx in db.sorted_values(by=[f"{values['-ALGO2-']}_score"], ascending=False).index]
        # compare_result = Spearman_s_Footrule(rank_1, rank_2)
        pass
        
_VARS['window'].close()
