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
m1 = df.iloc[0,0]
T1 = df.iloc[1,0]
m2 = df.iloc[2,0]
T2 = df.iloc[3,0]
Tf = df.iloc[4,0]

sigma_m1=0.1
sigma_T1=0.1
sigma_m2=0.1
sigma_T2=0.2
sigma_Tf=0.2

#print(df)

Me=m2*(T2-Tf)/(Tf-T1)-m1

# print(Me)

sigma_T_corr = 0.1  # °C, è un offset, non avendo avuto tempo per fare il fit di calibrazione non si ha idea, e neanche si può ipotizzare,
                    # un eventuale errore di scala

# Derivate parziali di Me
D    = Tf - T1
d_m1 = -1.0
d_m2 = (T2 - Tf) / D
d_T1 = m2 * (T2 - Tf) / D**2
d_T2 = m2 / D
d_Tf = m2 * (T1 - T2) / D**2

# Varianza di Me (diagonale + covarianze tra T1, T2, Tf)
u2_Me = (d_m1 * sigma_m1)**2 \
      + (d_m2 * sigma_m2)**2 \
      + (d_T1 * sigma_T1)**2 \
      + (d_T2 * sigma_T2)**2 \
      + (d_Tf * sigma_Tf)**2 \
      + 2 * sigma_T_corr**2 * (d_T1*d_T2 + d_T1*d_Tf + d_T2*d_Tf)

u_Me = np.sqrt(u2_Me)

print(f"Fattore di Correlazione del Termomento assunto costante: {sigma_T_corr}\nMe = {Me:.3f} ± {u_Me:.3f} g\n")

#vabè aggiungo uno z test perché si

Me_rif=25
sigma_Me_rif=5

comp=(abs(Me-Me_rif))/(sigma_Me_rif**2 + u_Me**2)
print(f"Test di compatiblità = {comp:.3f}\n")

#test con ipotesi di correlazione nulla e termometro assunto perfetto (come in realtà non è)


# Incertezze globali (risoluzione strumento)
sigma_m1 = 0.1   # g
sigma_m2 = 0.1   # g
sigma_T  = 0.2   # °C  (uguale per T1, T2, Tf)

# Derivate parziali di Me
D    = Tf - T1
d_m1 = -1.0
d_m2 = (T2 - Tf) / D
d_T1 = m2 * (T2 - Tf) / D**2
d_T2 = m2 / D
d_Tf = m2 * (T1 - T2) / D**2

# Varianza di Me: solo termini diagonali (covarianze nulle)
u2_Me = (d_m1 * sigma_m1)**2 \
      + (d_m2 * sigma_m2)**2 \
      + (d_T1 * sigma_T)**2 \
      + (d_T2 * sigma_T)**2 \
      + (d_Tf * sigma_T)**2

u_Me = np.sqrt(u2_Me)

print(f"Fattore di Correlazione del Termomento assunto costante: 0.0\nMe = {Me:.3f} ± {u_Me:.3f} g")
comp=(abs(Me-Me_rif))/(sigma_Me_rif**2 + u_Me**2)
print(f"Test di compatiblità = {comp:.3f}\n")


