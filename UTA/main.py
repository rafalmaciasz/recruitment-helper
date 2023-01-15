from uta import *
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # df = pd.read_csv('SWD_DB_test.csv',sep=',',decimal=',') 
    # df = df.fillna(1)
    # df["Procent zdawalności (0-100)"]=df["Procent zdawalności (0-100)"].str.replace(',','.')
    # df["Próg rekrutacji w poprzednim roku (0-100)"]=df["Próg rekrutacji w poprzednim roku (0-100)"].str.replace(',','.')
    # criteria = df[["Procent zdawalności (0-100)","Ocena absolwentów (1-5)","Własna ocena sylabusa (1-5)","Próg rekrutacji w poprzednim roku (0-100)"]]
    # criteria.rename(columns = {'Procent zdawalności (0-100)':'PZ','Ocena absolwentów (1-5)':'OA', 'Własna ocena sylabusa (1-5)':'WOS',
    #                           'Próg rekrutacji w poprzednim roku (0-100)':'PR'}, inplace = True)
    # # df.apply(lambda x: x.str.replace(',','.'))
    # # criteria = criteria.astype(float)
    # points =[]
    # for index, rows in criteria.iterrows():
    #     my_list =[rows.PZ, rows.OA, rows.WOS, rows.PR]
    #     points.append(my_list)
    
    # # print(points)
    # points = np.array(points)
    
    
    test_points = np.array([[3.6,4,4399,4],[3.7,12,8199,4],[3.9, 13, 8299,4],[4.5, 6, 7299,6],[3.5, 11, 5399,8],[4.6, 10, 7699,26],[3.1, 17, 4049,78],[3.6, 13, 3200,86],[3.7, 15, 5699,2],[4.2, 17, 7399,32],[4.6, 14, 5099,54],[4.2, 14, 5099,10],[4.7, 10, 5099,63],[5.1, 20, 10499,82]])
    min,max = get_min_max(test_points)
    max_or_min = [1,1,1,0]            # jeśli 1 to maksymalizujemy kryterium, jeśli 0 minimalizujemy

    # Wartości funkcji użyteczności dobrane ręcznie, kod umożliwia
    # dobranie funkcji użyteczności proporcjonalnie, dla takiego przypadku
    # współczynniki a i b wychodzą takie same dla wszystkich przedziałów

    func_utility = [[0.25,0.15,0],[0.25,0.2,0.15,0.10,0],[0.25,0.2,0.15,0.10,0],[0.25,0.15,0]]
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
    for i in test_points:
        score.append(rank([u1,u2,u3,u4],compartments,i))
    # print(np.array(score))

    
    # plt.title('Wartości funkcji użyteczności dla PZ')
    # plot_f_utility(u1,data_u1)
    
    # plt.title('Wartości funkcji użyteczności dla OA')
    # plot_f_utility(u2,data_u2)
    
    # plt.title('Wartości funkcji użyteczności dla WOS')
    # plot_f_utility(u3,data_u3)
    
    # plt.title('Wartości funkcji użyteczności dla PR')
    # plot_f_utility(u4,data_u4)
    