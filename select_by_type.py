import pandas as pd

def select(csv_name: str):
    db = pd.read_csv(csv_name)
    av_types = ["tech", "hum", "lek", "sci", "ekon", "spo", "sport", "wojs"]
    
    for type in av_types:
        type_db = db.loc[db["Rodzaj kierunku"] == type]
        type_db.to_csv(f"./datasets/{type}.csv", index=False)
    
    pass