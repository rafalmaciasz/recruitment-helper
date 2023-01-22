import numpy as np
from FuzzyNum import *
from fuzzy_topsis import fuzzy_topsis
from typing import List
import pandas as pd

def translate_to_fuzzy_preferences(grade : int):
    if grade == 1:
        return FuzzyNumb(1,1,3)
    elif grade == 2:
        return FuzzyNumb(1,2,4)
    elif grade == 3:
        return FuzzyNumb(1,3,5)
    elif grade == 4:
        return FuzzyNumb(2,4,6)
    elif grade == 5:
        return FuzzyNumb(3,5,7)
    elif grade == 6:
        return FuzzyNumb(4,6,8)
    elif grade == 7:
        return FuzzyNumb(5,7,9)
    elif grade == 8:
        return FuzzyNumb(6,8,9)
    elif grade == 9:
        return FuzzyNumb(7,9,9)
    else:
        raise ValueError("Nieprawidłowa wartość wagi")

def one_to_five_translation(grade : int):
    if grade == 1:
        return FuzzyNumb(1,1,3)
    elif grade == 2:
        return FuzzyNumb(1,3,5)
    elif grade == 3:
        return FuzzyNumb(3,5,7)
    elif grade == 4:
        return FuzzyNumb(7,9,10)
    elif grade == 5:
        return FuzzyNumb(9,10,10)
    else:
        raise ValueError(f"ocena poza skalą: grade = {grade}")



def translate_value(data_frame) -> List[List[FuzzyNumb]]:
    df : pd.DataFrame = data_frame[["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa","Ilość semestrów","Próg rekrutacji"]]
    df = df.to_numpy()
    D : List[List[FuzzyNumb]] = []
    for j in range(df.shape[0]):
        D.append([])
        for n,i in enumerate(["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa","Ilość semestrów","Próg rekrutacji"]):
            if i == "Procent zdawalności":
                x = -np.log(1-(df[j,n]/100))
                D[j].append(FuzzyNumb(100*max(1-np.exp(-(x-1)),0),df[j,n],100*(1-np.exp(-(x+1)))))
            elif i == "Ocena absolwentów":
                D[j].append(one_to_five_translation(df[j,n]))
            elif i == "Własna ocena sylabusa":
                D[j].append(one_to_five_translation(df[j,n]))
            elif i == "Ilość semestrów":
                D[j].append(FuzzyNumb(df[j,n],df[j,n],df[j,n]+2))
            elif i == "Próg rekrutacji":
                D[j].append(FuzzyNumb(max(df[j,n]-10,0),df[j,n],min(df[j,n]+10,100)))
    return D
    pass



def fuzzy_topsis_do_gui(weights : List[int],data_frame : pd.DataFrame,max_min : List[str]):
    """
    args:
        weights : List[int] - list that contains nombers 1-9 where 9 is Absolutely important and 1 is Equally important
        data_frame : df.DataFrame - data from database
        max_min : List[str] - list of strings for each collumn: "max" for profit , "min" for cost 
    return:
        List[Tuple[int,float]] - ranking of decision first is an index of decision second is a scoring function.
    """
    weights = [translate_to_fuzzy_preferences(i) for i in weights]
    D = translate_value(data_frame)
    if len(weights) != len(max_min):
        raise ValueError(f"Nie zgadzają się wymiary długość wag = {len(weights)}, długość data_frame = {data_frame.shape[1]}, długość max_min = {len(max_min)}")
    return fuzzy_topsis(D,weights,max_min)



if __name__ == '__main__':
    df = pd.read_csv("./datasets/lek.csv")
    print(fuzzy_topsis_do_gui([1,1,1,1,1],df,["max","min","max","max","max"]))
    pass



    """D1=[[FuzzyNumb(3,5,7),FuzzyNumb(7,9,9), FuzzyNumb(5,7,9)],
    [FuzzyNumb(5,7,9),FuzzyNumb(7,9,9), FuzzyNumb(3,5,7)],
    [FuzzyNumb(7,9,9),FuzzyNumb(3,5,7), FuzzyNumb(1,3,5)],
    [FuzzyNumb(1,3,5),FuzzyNumb(3,5,7), FuzzyNumb(1,1,3)]]

    D=[[FuzzyNumb(3,5.667,9), FuzzyNumb(5,8.333,9), FuzzyNumb(5,7,9)],
    [FuzzyNumb(5,7,9),FuzzyNumb(3,7,9), FuzzyNumb(3,5,7)],
    [FuzzyNumb(5,8.333,9),FuzzyNumb(3,5,7), FuzzyNumb(1,2.333,5)],
    [FuzzyNumb(1,2.333,5),FuzzyNumb(1,4.333,7), FuzzyNumb(1,1,3)]]

    w=[FuzzyNumb(5,7,9),FuzzyNumb(7,9,9),FuzzyNumb(3,5,7)]

    print(fuzzy_topsis(D,w,["max","max","min"]))"""


    """
    oceny - analiza leksykalna
    zdawalność - warości przedziałowe i jakieś odchylenie w przedziale
    trudność w dostaniu się - skala dyskretna - (analiza leksykalna)
    """