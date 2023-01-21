import pandas as pd

def convert2float(csv_name: str, column:str):
    db = pd.read_csv(f"./datasets/{csv_name}")
    db[column] = db[column].astype(float)
    db.to_csv(f"./datasets/{csv_name}")
    return