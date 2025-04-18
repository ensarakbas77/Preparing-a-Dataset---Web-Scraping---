import pandas as pd
import numpy as np

df = pd.read_excel("sorted_Tottenham.xlsx")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(f"\nVeri seti boyutu: {df.shape}")
print(df.head(5))

"""
# Tarihe göre sıralama
df['Tarih'] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y %H:%M')

# Tarih sütununa göre sıralama (geçmişten günümüze)
df = df.sort_values(by='Tarih', ascending=True)
print(df.head())

df.to_excel("sorted_Tottenham.xlsx", index=False)
"""

# Feature Engineering

df['Şut Verimliliği'] = df['İsabetli Şut'] / df['Şut'].replace(0, np.nan)
df['Gol Farkı'] = df['Gol'] - df['Rakip Gol']

df['Sezon'] = df['Tarih'].dt.year
df['Ay'] = df['Tarih'].dt.month
df['Haftanın Günü'] = df['Tarih'].dt.dayofweek + 1

df['Son 5 Maç Gol Ort'] = df.groupby('Sezon')['Gol'].transform(lambda x: x.rolling(5, min_periods=1).mean())

print(df.head(5))


df.to_excel("Tottenham.xlsx", index=False)
