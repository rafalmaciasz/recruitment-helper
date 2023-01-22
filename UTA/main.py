from uta import *
import numpy as np
import pandas as pd 
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt

def uta():

    # df = pd.read_csv(f"./datasets/SWD_DB.csv")
    
    df = pd.read_csv(f"./datasets/SWD_DB.csv") 
    # df = df.fillna(1)
    # df["Procent zdawalności"]=df["Procent zdawalności"].str.replace(',','.')
    # df["Próg rekrutacji"]=df["Próg rekrutacji"].str.replace(',','.')
    criteria = df[["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa","Próg rekrutacji"]]
    criteria.rename(columns = {'Procent zdawalności':'PZ','Ocena absolwentów':'OA', 'Własna ocena sylabusa':'WOS',
                              'Próg rekrutacji':'PR'}, inplace = True)
    # df.apply(lambda x: x.str.replace(',','.'))
    # criteria = criteria.astype(float)
    points =[]
    for index, rows in criteria.iterrows():
        my_list =[rows.PZ, rows.OA, rows.WOS, rows.PR]
        points.append(my_list)
    
    # print(points)
    points = np.array(points)
    
    min,max = get_min_max(points)
    max_or_min = [1,1,1,0]            # jeśli 1 to maksymalizujemy kryterium, jeśli 0 minimalizujemy

    # Wartości funkcji użyteczności dobrane ręcznie, kod umożliwia
    # dobranie funkcji użyteczności proporcjonalnie, dla takiego przypadku
    # współczynniki a i b wychodzą takie same dla wszystkich przedziałów

    func_utility = [[0.25,0.02,0],[0.25,0.2,0.15,0.10,0],[0.25,0.2,0.15,0.10,0],[0.25,0.15,0]]
    compartments = split(min,max,np.array([2,4,4,2]),max_or_min,func_utility)
    # print(compartments)
    data_u1 = compartments[0] # Wartości funkcji użyteczności dla taktowania u1
    data_u2 = compartments[1] # Wartości funkcji użyteczności dla czasu pracy na baterii u2
    data_u3 = compartments[2] # Wartości funkcji użyteczności dla ceny u3
    data_u4 = compartments[3]
    # print(data_u1)
    u1 = function_value(data_u1,1)
    u2 = function_value(data_u2,1)
    u3 = function_value(data_u3,1)
    u4 = function_value(data_u4,0)
    # print(u1,'\n')
    # print(u2,'\n')
    # print(u3)
    score = []
    for i in points:
        score.append(rank([u1,u2,u3,u4],compartments,i))
    print(np.array(score))

    df['UTA_score'] = score
    # print(df.head(10))
    # plt.title('Wartości funkcji użyteczności dla PZ')
    # plot_f_utility(u1,data_u1)
    
    # plt.title('Wartości funkcji użyteczności dla OA')
    # plot_f_utility(u2,data_u2)
    
    # plt.title('Wartości funkcji użyteczności dla WOS')
    # plot_f_utility(u3,data_u3)
    
    # plt.title('Wartości funkcji użyteczności dla PR')
    # plot_f_utility(u4,data_u4)

uta()