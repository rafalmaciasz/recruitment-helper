from typing import List,Callable
from spcs import norm, SPCS
import pandas as pd
import numpy as np

if __name__ == '__main__':
    df_og = pd.read_csv("C:\studia\sem_5\SWD\projekt/recruitment-helper\datasets\ekon.csv")
    lst = ["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa"]
    df : pd.DataFrame = df_og[lst]
    num = df.to_numpy()
    ide = []
    aide = []
    for i in lst:
        ddf = df.sort_values([i])
        aide.append((ddf.iloc[-1]).to_numpy())
        ide.append((ddf.iloc[0]).to_numpy())
    rep = SPCS(ide,aide,num)
    df_kon = df_og.assign(Wartosc=rep)
    print(df_kon.sort_values('Wartosc',ascending=False))
    pass

def gui_spc(df_og: pd.DataFrame):
    lst = ["Procent zdawalności","Ocena absolwentów","Własna ocena sylabusa"]
    df : pd.DataFrame = df_og[lst]
    num = df.to_numpy()
    ide = []
    aide = []
    for i in lst:
        ddf = df.sort_values([i])
        aide.append((ddf.iloc[-1]).to_numpy())
        ide.append((ddf.iloc[0]).to_numpy())
    rep = SPCS(ide,aide,num)
    df_kon = df_og.assign(Wartosc=rep)
    return df_kon.sort_values('Wartosc',ascending=False)

