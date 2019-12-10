import os 
import pandas as pd

inspection = pd.read_csv(os.path.join(os.path.dirname(__file__), "./data/clean_data/combined.csv"),
                           low_memory=False)