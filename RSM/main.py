from typing import List,Callable
import numpy as np
import pandas as pd
from comp_rank import kom_rank

dfA = pd.read_excel("RSM.xlsx", "A",header=None)
dfB = pd.read_excel("RSM.xlsx", "B",header=None)
# print(dfA)
A=dfA.values.tolist()
B=dfB.values.tolist()
# print(A, '\n', B)



min_max=[]
for i in range(len(A[0])):
    a=input("Podaj kryterium(min lub max): ")
    if (a=="min" or a=="max"):
        min_max.append(np.min if a == "min" else np.max)
    else:
        raise ValueError("Zła wartosc")
kom_rank(A,B,min_max)