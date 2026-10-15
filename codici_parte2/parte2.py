import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("Dati e annotazioni - 0.3.csv",
                 header=None,          # nessuna intestazione
                 decimal=",",          # virgola come separatore decimale
                 quotechar='"')        # gestisce le virgolette

## print(df)
# prima riga -> array di 4 double
ma = df.iloc[0].to_numpy(dtype=np.float64)
Ta = df.iloc[1].to_numpy(dtype=np.float64)
mg = df.iloc[2].to_numpy(dtype=np.float64)
Tf = df.iloc[3].to_numpy(dtype=np.float64)

Me = 25
sigma_Me=5

sigma_ma = np.zeros(4)
sigma_Ta = np.zeros(4)
sigma_mg = np.zeros(4)
sigma_Tf = np.zeros(4)

lam = np.zeros(4)          # array di 4 double, inizializzati a 0

for i in range(4):         # i = 0, 1, 2, 3
    lam[i] = 1 * ( (ma[i] + Me) * (Ta[i] - Tf[i]) - mg[i] * (Tf[i] - 0) ) / mg[i]
    print(lam[i])
