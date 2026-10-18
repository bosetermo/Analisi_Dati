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
m2 = df.iloc[0,0]
T2 = df.iloc[1,0]
m1 = df.iloc[2,0]
T1 = df.iloc[3,0]
Tf = df.iloc[4,0]

#print(df)

Me=m2*(T2-Tf)/(Tf-T1)-m1
print(Me)

#esce un risultato negativo seguendo l'ordine delle masse scritto nell'excel. Qui, come quando
#abbiamo verificato le misure in laboratorio, abbiamo fatto un macello con m1 e m2 (Filippo boia)
#faccio un nuovo pytohn con i risultati sensati. Questo lo lascio perché si
