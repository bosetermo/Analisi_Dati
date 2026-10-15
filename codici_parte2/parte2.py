import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("Dati e annotazioni - 0.3.csv",
                 header=None,          # nessuna intestazione
                 decimal=",",          # virgola come separatore decimale
                 quotechar='"')        # gestisce le virgolette

print(df)
