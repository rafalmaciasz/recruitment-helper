import PySimpleGUI as sg
import pandas as pd
import csv
_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False}

list_m=['TOPSIS','RSM',"SAFETY PRINCIPAL","UTA"]
list_k =['Miasto', 'Nazwa kierunku', 'Nazwa uczelni',
       'Procent zdawalności (0-100)', 'Ocena absolwentów (1-5)',
       'Własna ocena sylabusa (1-5)', 'Ilość semestrów',
       'Próg rekrutacji w poprzednim roku (0-100)',
       'Rodzaj kierunku (tech. hum. ekon. itd)']
list_kryt=["Kry "+str(i) for i in range(len(list_k))]
td=[]
layout_1 =[[
    sg.Button("Wczytaj dane z pliku",key="-BUTTON_INSERT-"),
    sg.Combo(key='-COMBO-',values=list_m,default_value=list_m[0]),
    sg.Button("Stwórz ranking",key='-BUTTON_RANKING-')]]
layout_2=    [[sg.Text("Alternatywy z kryteriami",justification='center')],
    [sg.Table(values=td,headings= list_k,key="-TABLE_KRYT-",max_col_width = 5, auto_size_columns = True,vertical_scroll_only=False,justification = 'center',expand_x=True,expand_y=True)]]
layout_3 =   [[sg.Text("Klasy",justification='center')],
    [sg.Table([], ['Col 1','Col 2','Col 3'], num_rows=2)]]
layout_4 = [[sg.Table([], ['Col 1','Col 2','Col 3'], num_rows=2)]]
layout = [[layout_1],
          [sg.Col(layout_3,vertical_alignment='top'),sg.Col(layout_2,vertical_alignment='top')],
          [layout_4]]

_VARS['window'] = sg.Window('GUI_UwU',
                            layout,
                            finalize=True,
                            resizable=True,
                            size=(500,500),
                            element_justification="center")

while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == sg.WIN_CLOSED :
        break
    if event == "-BUTTON_INSERT-":
        with open("SWD_DB.csv", 'r') as file:
            data = csv.reader(file)
            list_of_csv = list(map(tuple, data))
        print(len(list_of_csv))
        if len(list_of_csv) != 0:
            sg.popup('Pobrano dane',line_width=40)
        else:
            sg.popup('Brak danych')
    if event == "-BUTTON_RANKING-":
        for i in range(1,len(list_of_csv)):
            td.append(list_of_csv[i])
        _VARS['window']['-TABLE_KRYT-'].update(values=td)
_VARS['window'].close()