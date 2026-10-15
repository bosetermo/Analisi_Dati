import pandas as pd
import numpy as np

# 1. PARAMETRI E INCERTEZZE STRUMENTALI
M_E = 25.0       # g
C_W = 1.00       # cal/(g*°C)

# Incertezze sugli strumenti
DELTA_M = 0.1    # Incertezza massa bilancia (g)
DELTA_ME = 5.0   # Incertezza equivalente in acqua thermos (g)
DELTA_T = 0.2    # Incertezza termometro (°C)

NOME_FILE = 'Dati e annotazioni - 0.2 Al.csv'

# 2. LETTURA CSV DISPOSTO PER RIGHE E TRASPOSIZIONE
df_raw = pd.read_csv(NOME_FILE, header=None, sep=None, decimal=',', engine='python')
df = df_raw.T.copy()
df.columns = ['materiale', 'T1', 'm_a', 'm_c', 'Ta', 'Tf']

colonne_numeriche = ['m_c', 'm_a', 'T1', 'Ta', 'Tf']
df[colonne_numeriche] = df[colonne_numeriche].astype(float)

# 3. CALCOLO CALORE SPECIFICO (c)
df['c'] = ((df['m_a'] + M_E) * C_W * (df['Tf'] - df['Ta'])) / (df['m_c'] * (df['T1'] - df['Tf']))

# 4. PROPAGAZIONE ANALITICA DELL'ERRORE PER OGNI RIGA
def calcola_errore_propagato(row):
    mc, ma = row['m_c'], row['m_a']
    t1, ta, tf = row['T1'], row['Ta'], row['Tf']
    c_val = row['c']
    
    # Derivate parziali
    dc_dma = c_val / (ma + M_E)
    dc_dme = c_val / (ma + M_E)
    dc_dmc = -c_val / mc
    dc_dta = -c_val / (tf - ta)
    dc_dt1 = -c_val / (t1 - tf)
    dc_dtf = c_val * (1.0 / (tf - ta) + 1.0 / (t1 - tf))
    
    # Somma in quadratura dei contributi
    var_c = (
        (dc_dma * DELTA_M)**2 +
        (dc_dme * DELTA_ME)**2 +
        (dc_dmc * DELTA_M)**2 +
        (dc_dta * DELTA_T)**2 +
        (dc_dt1 * DELTA_T)**2 +
        (dc_dtf * DELTA_T)**2
    )
    return np.sqrt(var_c)

df['sigma_prop'] = df.apply(calcola_errore_propagato, axis=1)

# 5. SINTESI FINALE ED ERRORE COMBINATO
n_misure = len(df)
c_medio = df['c'].mean()
s_stat = df['c'].std()                              # Deviazione standard
sigma_stat_media = s_stat / np.sqrt(n_misure)      # Errore standard della media
sigma_prop_media = df['sigma_prop'].mean()          # Incertezza sistematica media
sigma_totale = np.sqrt(sigma_stat_media**2 + sigma_prop_media**2) # Incertezza combinata

print("=== RISULTATI DETTAGLIATI PER MISURA ===")
print(df[['m_c', 'm_a', 'T1', 'Ta', 'Tf', 'c', 'sigma_prop']])

print("\n=== SINTESI ED INCERTEZZA FINALE ===")
print(f"Calore specifico medio (c) : {c_medio:.3f} cal/(g °C)")
print(f"Incertezza statistica media: {sigma_stat_media:.3f} cal/(g °C)")
print(f"Incertezza sistematica media : {sigma_prop_media:.3f} cal/(g °C)")
print(f"Incertezza TOTALE combinata : {sigma_totale:.3f} cal/(g °C)")
print(f"Risultato: c = ({c_medio:.3f} ± {sigma_totale:.3f}) cal/(g °C)")
