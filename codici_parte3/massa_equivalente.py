import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("Dati e annotazioni - 0.7.csv",
                 header=None,          # nessuna intestazione
                 decimal=",",          # virgola come separatore decimale
                 quotechar='"')        # gestisce le virgolette

## print(df)
# prima riga -> array di 4 double
m2 = df.iloc[0].to_numpy(dtype=np.float64)
T2 = df.iloc[1].to_numpy(dtype=np.float64)
m1 = df.iloc[2].to_numpy(dtype=np.float64)
T1 = df.iloc[3].to_numpy(dtype=np.float64)
Tf = df.iloc[4].to_numpy(dtype=np.float64)

sigma_ma = 0.1
sigma_Ta = 0.2
sigma_mg = 0.1
sigma_Tf = 0

Me=((m2*(T2-Tf))/(Tf-T1))-m1
print(Me)
