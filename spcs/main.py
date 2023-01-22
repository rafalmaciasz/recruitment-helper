from typing import List,Callable
from spcs import norm, SPCS
import pandas as pd
import numpy as np

if __name__ == '__main__':
    min_max = [np.max,np.min,np.min]
    Ide = np.array([[64,4000,10],[32,5000,25],[16,4000,20]])
    AIde = np.array([[8,8000,35],[16,7000,100],[32,10000,50]])
    badane = np.array([[16,8000,35],[32,6000,70],[8,4500,21],[8,5000,30]])
    print(SPCS(Ide,AIde,badane))

def gui_spc(weights):

    pass

# if __name__ == '__main__':
#     df = pd.read_csv('./datasets/lek.csv')