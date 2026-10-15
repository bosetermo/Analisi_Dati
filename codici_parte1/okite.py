import pandas as pd
import numpy as np

# 1. PARAMETRI COSTANTI DELL'ESPERIMENTO
M_E = 25.0    # Massa equivalente in acqua del thermos (in grammi)
C_W = 1.00    # Calore specifico dell'acqua in cal/(g * °C)

NOME_FILE = 'Dati e annotazioni - 0.2 Okite.csv'

# 2. LETTURA CSV DISPOSTO PER RIGHE E TRASPOSIZIONE
df_raw = pd.read_csv(
    NOME_FILE, 
    header=None, 
    sep=None, 
    decimal=',', 
    engine='python'
)

# Ruotiamo righe e colonne (trasposizione)
df_okite = df_raw.T.copy()

# Assegniamo i nomi alle righe rispettando l'ordine del CSV
nomi_colonne = ['materiale', 'T1', 'm_a', 'm_c', 'Ta', 'Tf']
df_okite.columns = nomi_colonne

# Convertiamo in float le colonne numeriche
colonne_numeriche = ['m_c', 'm_a', 'T1', 'Ta', 'Tf']
df_okite[colonne_numeriche] = df_okite[colonne_numeriche].astype(float)

# 3. CALCOLO DEL CALORE SPECIFICO c IN CALORIE
# Formula: c = ((m_a + M_e) * c_w * (Tf - Ta)) / (m_c * (T1 - Tf))
df_okite['c_cal_gC'] = (
    (df_okite['m_a'] + M_E) * C_W * (df_okite['Tf'] - df_okite['Ta'])
) / (df_okite['m_c'] * (df_okite['T1'] - df_okite['Tf']))

# 4. STAMPA DELLE SINGOLE MISURE
print("=== MISURE DI DETTAGLIO OKITE (cal/(g * °C)) ===")
print(df_okite[['m_c', 'm_a', 'T1', 'Ta', 'Tf', 'c_cal_gC']])

# 5. ANALISI DELLA MEDIA E DISPERSIONE
n_misure = len(df_okite)
media = df_okite['c_cal_gC'].mean()
dev_std = df_okite['c_cal_gC'].std()
errore_std = dev_std / np.sqrt(n_misure) if n_misure > 0 else 0

print("\n=== SINTESI STATISTICA OKITE ===")
print(f"Numero di misure valide : {n_misure}")
print(f"Calore specifico medio  : {media:.6f} cal/(g °C)")
print(f"Deviazione standard (s) : {dev_std:.6f} cal/(g °C)")
print(f"Errore standard media   : {errore_std:.6f} cal/(g °C)")
