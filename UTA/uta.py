import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

def getMinMax(inputPoints: np.ndarray):
    x, y = inputPoints.shape
    min = 100000* np.ones(y)
    max = np.zeros(y)
    for i in range(x): # iteruj po punktach
        for j in range(y): # iteruj po parametrach punktu
            a = inputPoints[i,j]
            b = min[j]
            if inputPoints[i,j] < min[j]:
                min[j] = inputPoints[i,j]
            if inputPoints[i,j] > max[j]:
                max[j] = inputPoints[i,j]

    return min,max

def split(min,max,partitions,max_or_min,func_utility = None):
    list = []
    alternatives = len(partitions) # ilość kryteriów
    for i in range(alternatives):
        row = [(0,0)]*(partitions[i]+1)
        list.append(row)

    func_utility_max = 1/alternatives  # maksymalna wartość funkcji użytecznosci przy danej liczbie kryteriów
    
    if not func_utility: 
        for i in range(alternatives):
            if max_or_min[i] == 0: # jeśli minimalizujemy   
                list[i][0] = (min[i],func_utility_max) # wpisuje maxymalną i minimalna wartość kryterium
                list[i][-1] = (max[i],0)
                diff = max[i] - min[i]      # obliczam różnice miedzy max a min wartością kryterium
                compartment = diff/partitions[i]    # wyznaczam przedziały 
                func_utility_other = func_utility_max/partitions[i] # wyznaczam wartość f. użyteczności dla przedziałów
                for j in range(1,partitions[i]): # wpisuje wartości dla konkretnych przedziałów
                    list[i][j] = (min[i]+ j*compartment,func_utility_max -func_utility_other*j)
            

            if max_or_min[i] == 1: # jeśli maksymalizujemy
                list[i][0] = (max[i],func_utility_max) 
                list[i][-1] = (min[i],0)
                diff = max[i] - min[i]
                compartment = diff/partitions[i]
                func_utility_other = func_utility_max/partitions[i]
                for j in range(1,partitions[i]):
                    list[i][j] = (max[i] - j*compartment,func_utility_max - func_utility_other*j)
    else:
        for i in range(alternatives):
            if max_or_min[i] == 0: # jeśli minimalizujemy   
                list[i][0] = (min[i],func_utility[i][0]) # wpisuje maksymalną i minimalna wartość kryterium
                list[i][-1] = (max[i],func_utility[i][-1])
                diff = max[i] - min[i]      # obliczam różnice miedzy max a min wartością kryterium
                compartment = diff/partitions[i]    # wyznaczam przedziały 
                for j in range(1,partitions[i]): # wpisuje wartości dla konkretnych przedziałów
                    list[i][j] = (min[i]+ j*compartment,func_utility[i][j])
            

            if max_or_min[i] == 1: # jeśli maksymalizujemy
                list[i][0] = (max[i],func_utility[i][0]) 
                list[i][-1] = (min[i],func_utility[i][-1])
                diff = max[i] - min[i]
                compartment = diff/partitions[i]
                for j in range(1,partitions[i]):
                    list[i][j] = (max[i] - j*compartment,func_utility[i][j])

    return list

def function_value(compartments,max_or_min):
    list = []
    idx = len(compartments) - 1
    for i in range(1,len(compartments)):
        if max_or_min == 1: # maksymalizacja
            a = (compartments[(idx-i+1)][1]-compartments[(idx-i)][1])/(compartments[(idx-i+1)][0]-compartments[(idx-i)][0])
            b = compartments[(idx-i+1)][1]-a*compartments[(idx-i+1)][0]
            list.append([a,b])
        
        if max_or_min == 0: # minimalizacja
            a = (compartments[i-1][1]-compartments[i][1])/(compartments[i-1][0]-compartments[i][0])
            b = compartments[(i-1)][1]-a*compartments[(i-1)][0]
            list.append([a,b])
    
    return list

def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

def plot_f_utility(u,compartments): # u - lista współczynników a i b dla f.użyteczności
    cmap = get_cmap(len(u)+1)
        
    for i in range(len(u)):
        a,b = u[i]
        x = np.linspace(compartments[i][0],compartments[i+1][0],100)
        y = a*x+b
        if i == len(u)-1:
            plt.scatter(compartments[len(u)][0],a*compartments[len(u)][0]+b, c = 'blue')
        plt.scatter(compartments[i][0],a*compartments[i][0]+b, c = 'blue')
        plt.plot(x, y, c =cmap(i))
        

    plt.grid()
    plt.show()

def rank(utility_coef, compartments, point):
    score = 0  
    for i in range(len(compartments[0])):
        for j in range(len(compartments[i])-1):
            # a = point[i]
            # x = compartments[i][j][0]
            # y = compartments[i][j+1][0]
            if point[i] <= compartments[i][j][0] and point[i] >= compartments[i][j+1][0]:
                score += utility_coef[i][j][0]*point[i]+utility_coef[i][j][1]

            elif point[i] >= compartments[i][j][0] and point[i] <= compartments[i][j+1][0]:
                score += utility_coef[i][j][0]*point[i]+utility_coef[i][j][1]

    return score
    

def main():
    df = pd.read_csv('SWD_DB_test.csv',sep=',',decimal=',') 
    df = df.fillna(1)
    df["Procent zdawalności (0-100)"]=df["Procent zdawalności (0-100)"].str.replace(',','.')
    df["Próg rekrutacji w poprzednim roku (0-100)"]=df["Próg rekrutacji w poprzednim roku (0-100)"].str.replace(',','.')
    criteria = df[["Procent zdawalności (0-100)","Ocena absolwentów (1-5)","Własna ocena sylabusa (1-5)","Próg rekrutacji w poprzednim roku (0-100)"]]
    criteria.rename(columns = {'Procent zdawalności (0-100)':'PZ','Ocena absolwentów (1-5)':'OA', 'Własna ocena sylabusa (1-5)':'WOS',
                              'Próg rekrutacji w poprzednim roku (0-100)':'PR'}, inplace = True)
    # df.apply(lambda x: x.str.replace(',','.'))
    # criteria = criteria.astype(float)
    points =[]
    for index, rows in criteria.iterrows():
        my_list =[rows.PZ, rows.OA, rows.WOS, rows.PR]
        points.append(my_list)
    
    # print(points)
    points = np.array(points)
    test_points = np.array([[3.6,4,4399,4],[3.7,12,8199,4],[3.9, 13, 8299,4],[4.5, 6, 7299,6],[3.5, 11, 5399,8],[4.6, 10, 7699,26],[3.1, 17, 4049,78],[3.6, 13, 3200,86],[3.7, 15, 5699,2],[4.2, 17, 7399,32],[4.6, 14, 5099,54],[4.2, 14, 5099,10],[4.7, 10, 5099,63],[5.1, 20, 10499,82]])
    min,max = getMinMax(test_points)
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
    
main()