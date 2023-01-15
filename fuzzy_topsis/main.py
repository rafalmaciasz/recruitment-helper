import numpy as np
from FuzzyNum import *
from fuzzy_topsis import fuzzy_topsis

D1=[[FuzzyNumb(3,5,7),FuzzyNumb(7,9,9), FuzzyNumb(5,7,9)],
[FuzzyNumb(5,7,9),FuzzyNumb(7,9,9), FuzzyNumb(3,5,7)],
[FuzzyNumb(7,9,9),FuzzyNumb(3,5,7), FuzzyNumb(1,3,5)],
[FuzzyNumb(1,3,5),FuzzyNumb(3,5,7), FuzzyNumb(1,1,3)]]

D=[[FuzzyNumb(3,5.667,9), FuzzyNumb(5,8.333,9), FuzzyNumb(5,7,9)],
[FuzzyNumb(5,7,9),FuzzyNumb(3,7,9), FuzzyNumb(3,5,7)],
[FuzzyNumb(5,8.333,9),FuzzyNumb(3,5,7), FuzzyNumb(1,2.333,5)],
[FuzzyNumb(1,2.333,5),FuzzyNumb(1,4.333,7), FuzzyNumb(1,1,3)]]

w=[FuzzyNumb(5,7,9),FuzzyNumb(7,9,9),FuzzyNumb(3,5,7)]

print(fuzzy_topsis(D,w,["max","max","min"]))


"""
oceny - analiza leksykalna
zdawalność - warości przedziałowe i jakieś odchylenie w przedziale
trudność w dostaniu się - skala dyskretna - (analiza leksykalna)
"""