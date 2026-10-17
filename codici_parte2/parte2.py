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
# 3) Matrice di covarianza (Me è errore comune a tutte le misure)
#    C_ij = δ_ij · u²_cas(λ_i)  +  σ²_Me · d_Me,i · d_Me,j
# ------------------------------------------------------------
C    = np.diag(u2_cas) + (sigma_Me**2) * np.outer(d_Me, d_Me)
Cinv = np.linalg.inv(C)

# ------------------------------------------------------------
# 4) Media pesata generalizzata (GLS / MLE)
# ------------------------------------------------------------
N    = len(lam)
ones = np.ones(N)

lam_bar   = (ones @ Cinv @ lam) / (ones @ Cinv @ ones)
u_lam_bar = 1.0 / np.sqrt(ones @ Cinv @ ones)

print(f"\n--- Risultato globale (GLS) ---")
print(f"λ̄ = {lam_bar:.3f} ± {u_lam_bar:.3f} cal/g")

# Confronto: media pesata SENZA covarianza (per vedere la differenza)
w_simple      = 1.0 / u2_lam
lam_bar_s     = np.sum(w_simple * lam) / np.sum(w_simple)
u_lam_bar_s   = 1.0 / np.sqrt(np.sum(w_simple))
print(f"   (senza covarianza sarebbe: {lam_bar_s:.3f} ± {u_lam_bar_s:.3f} cal/g)")

# ------------------------------------------------------------
# 5) Test del chi quadro
# ------------------------------------------------------------
r    = lam - lam_bar
chi2 = r @ Cinv @ r
dof  = N - 1

if dof > 0:
    p_value = 1 - stats.chi2.cdf(chi2, dof)
    print(f"\n--- Test di consistenza ---")
    print(f"chi²/dof = {chi2:.2f}/{dof}  ->  chi²/dof = {chi2/dof:.2f}")
    print(f"p-value  = {p_value:.3f}")

    # Birge ratio se il chi² è alto
    if chi2 / dof > 1:
        R = np.sqrt(chi2 / dof)
        u_lam_bar_birge = u_lam_bar * R
        print(f"Birge ratio R = {R:.2f}  ->  u(λ̄) corretta = {u_lam_bar_birge:.3f} cal/g")
    else:
        print("Incertezze compatibili con la dispersione dei dati.")
else:
    print("\nCon N = 1 non è possibile calcolare il chi².")