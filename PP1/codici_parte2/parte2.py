import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

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

sigma_ma = 0.1
sigma_Ta = 0.2
sigma_mg = 0.1
sigma_Tf = 0

lam = np.zeros(4)          # array di 4 double, inizializzati a 0

for i in range(4):         # i = 0, 1, 2, 3
    lam[i] = 1 * ( (ma[i] + Me) * (Ta[i] - Tf[i]) - mg[i] * (Tf[i] - 0) ) / mg[i]
    print(lam[i])

    # ============================================================
# PROPAGAZIONE INCERTEZZE E MEDIA PESATA GENERALIZZATA (GLS)
# ============================================================

# Costanti fisiche
Tg   = 0.0    # °C, ghiaccio a 0 °C
ca   = 1.0    # cal/(g·K)
sigma_Tg = 0.2 
sigma_ca = 0.0  # assunto esatto

# ------------------------------------------------------------
# 1) Derivate parziali di lambda rispetto a ogni variabile
# ------------------------------------------------------------
d_ma =  ca * (Ta - Tf) / mg
d_Me =  ca * (Ta - Tf) / mg
d_Ta =  ca * (ma + Me) / mg
d_Tf = -ca * (ma + Me + mg) / mg
d_mg = -ca * (ma + Me) * (Ta - Tf) / mg**2
d_Tg =  ca * np.ones_like(lam)
d_ca =  lam / ca

# ------------------------------------------------------------
# 2) Varianza "casuale" per ogni misura (escluso Me)
# ------------------------------------------------------------
u2_cas = (d_ma * sigma_ma)**2 + (d_Ta * sigma_Ta)**2 + \
         (d_Tf * sigma_Tf)**2 + (d_mg * sigma_mg)**2 + \
         (d_Tg * sigma_Tg)**2 + (d_ca * sigma_ca)**2

# Incertezza individuale completa (include il contributo di Me)
u2_lam = u2_cas + (d_Me * sigma_Me)**2
u_lam  = np.sqrt(u2_lam)

print("\n--- Incertezze individuali ---")
for i in range(len(lam)):
    print(f"Misura {i+1}: λ = {lam[i]:.3f} ± {u_lam[i]:.3f} cal/g")


# ------------------------------------------------------------
# 4) Media pesata generalizzata (GLS / MLE)
# ------------------------------------------------------------
N    = len(lam)
ones = np.ones(N)

lam_bar   = np.sum(lam / u2_lam) / np.sum(1.0 / u2_lam)
u_lam_bar = 1.0 / np.sqrt(np.sum(1.0 / u2_lam))

print(f"\n--- Risultato globale (GLS) ---")
print(f"λ̄ = {lam_bar:.3f} ± {u_lam_bar:.3f} cal/g")