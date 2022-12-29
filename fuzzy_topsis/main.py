import numpy as np
from Fuzzy_Num import *
from fuzzy_topsis import fuzzy_topsis

D1=np.ndarray([Fuzzy_Numb(3,5,7),Fuzzy_Numb(7,9,9), Fuzzy_Numb(5,7,9)],
[Fuzzy_Numb(5,7,9),Fuzzy_Numb(7,9,9), Fuzzy_Numb(3,5,7)],
[Fuzzy_Numb(7,9,9),Fuzzy_Numb(3,5,7), Fuzzy_Numb(1,3,5)],
[Fuzzy_Numb(1,3,5),Fuzzy_Numb(3,5,7), Fuzzy_Numb(1,1,3)], dtype = Fuzzy_Numb)

D=np.ndarray([Fuzzy_Numb(3,5.667,9),Fuzzy_Numb(5,8.333,9), Fuzzy_Numb(5,7,9)],
[Fuzzy_Numb(5,7,9),Fuzzy_Numb(3,7,9), Fuzzy_Numb(3,5,7)],
[Fuzzy_Numb(5,8.333,9),Fuzzy_Numb(3,5,7), Fuzzy_Numb(1,2.333,5)],
[Fuzzy_Numb(1,2.333,5),Fuzzy_Numb(1,4.333,7), Fuzzy_Numb(1,1,3)])

w=[Fuzzy_Numb(5,7,9),Fuzzy_Numb(7,9,9),Fuzzy_Numb(3,5,7)]

fuzzy_topsis(D,w,["max","max","min"])