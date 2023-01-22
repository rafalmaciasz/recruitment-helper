import PySimpleGUI as sg
import pandas as pd
from fuzzy_topsis import fuzzy_topsis
from RSM import RSM
# from SPCP import SPCP
# from UTA import UTA

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
    'UTA': '???'
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

weight_layout = [
    [sg.Text('Podaj wagi', justification='center')],
    [sg.Table(values=[sg.InputText(key=f'-IN{str(i)}-') for i in range(len(list_k))], headings=list_k)]
]

criteria_layout = [
    [sg.Text('Podaj kryteria', justification='center')],
    [sg.Table(values=[sg.InputText(key=f'-IN{str(i)}-') for i in range(len(list_k))], headings=list_k)]
]

#TODO dodac nazwy funkcji
additional_params = {
    'FUZZY TOPSIS': [weight_layout, criteria_layout],
    'RSM': criteria_layout,
    'SAFETY PRINCIPAL': '???',
    'UTA': '???'
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

disp_ranking_layout = [
    [sg.Text('Ranking',justification='center')],
    [sg.Table([], ['Nazwa kierunku','Wynik'], num_rows=2)]
]

layout = [
    [choose_type_layout],
    [choose_algo_layout],
    [create_rank_layout],
    
    [sg.Col(class_layout,vertical_alignment='top'),sg.Col(alternatives_layout,vertical_alignment='top')],
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
        
        # Load database
        db = pd.read_csv(f"./datasets/{types[values['-TYPE-']]}.csv", sep=',')
        
        # Call algorithm
        # rank = values['-ALGO-'](db, jakies_dodatkowe_gowno)

        _VARS['window']['-TABLE_KRYT-'].update(values=list(map(tuple, db.values)))
        
_VARS['window'].close()