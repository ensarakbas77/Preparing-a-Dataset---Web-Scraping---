import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

team_name = "Liverpool"

df = pd.read_excel(f"{team_name}.xlsx")


# Maç Sonuçlarının Sezonlara Göre Dağılımı
df['Tarih'] = pd.to_datetime(df['Tarih'])
df['Sezon'] = df['Tarih'].apply(lambda x: f"{x.year-1}/{x.year}" if x.month < 7 else f"{x.year}/{x.year+1}")
df['Sonuç'] = df.apply(lambda x: 'Galibiyet' if x['Gol'] > x['Rakip Gol'] else ('Mağlubiyet' if x['Gol'] < x['Rakip Gol'] else 'Beraberlik'), axis=1)

plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='Sezon', hue='Sonuç', palette='Set2')
plt.title(f"{team_name} - 2013/2014 ve 2024/2025 Arası Maç Sonuçları Dağılımı")
plt.xlabel("Sezon")
plt.ylabel("Maç Sayısı")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Atılan Gollerin Dağılımı
plt.figure(figsize=(8, 5))
sns.histplot(df['Gol'], bins=range(0, df['Gol'].max()+2), kde=False, color='skyblue')
plt.title(f"{team_name} - Atılan Gollerin Dağılımı")
plt.xlabel("Gol Sayısı")
plt.ylabel("Maç Sayısı")
plt.tight_layout()
plt.show()

# Ev Sahibi / Deplasman Performansları
ev_deplasman = df.groupby(['Is_Home', 'Sonuç']).size().unstack().fillna(0)
ev_deplasman.index = ['Deplasman', 'Ev Sahibi']

percent_df = ev_deplasman.div(ev_deplasman.sum(axis=1), axis=0) * 100

ax = ev_deplasman.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set3')

for idx, row in enumerate(ev_deplasman.values):
    total = sum(row)
    y_offset = 0
    for col_idx, val in enumerate(row):
        percent = percent_df.values[idx][col_idx]
        if val > 0:
            ax.text(idx, y_offset + val / 2, f"{percent:.1f}%", ha='center', va='center', fontsize=10, color='black')
            y_offset += val


plt.title(f"{team_name} - Ev Sahibi / Deplasman Performansları")
plt.ylabel("Maç Sayısı")
plt.xlabel("")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# Sezonlara Göre Galibiyet Yüzdesi ve Gol Ortalamaları

sns.set(style="whitegrid")

season_stats = df.groupby('Sezon').agg({
    'Sonuç': lambda x: (x == 'Galibiyet').mean() * 100,
    'Gol': 'mean',
    'Rakip Gol': 'mean'
}).reset_index()

plt.figure(figsize=(14, 6))

# 1. Grafik: Galibiyet yüzdesi
plt.subplot(1, 2, 1)
sns.lineplot(data=season_stats, x='Sezon', y='Sonuç', marker='o', color='green', linewidth=2)
plt.title(f'{team_name} - Sezonlara Göre Galibiyet Yüzdesi', fontsize=13)
plt.ylabel('Galibiyet (%)')
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.grid(True)

# 2. Grafik: Gol ortalamaları
plt.subplot(1, 2, 2)
sns.lineplot(data=season_stats, x='Sezon', y='Gol', marker='o', color='blue', label='Atılan Gol (Ort)', linewidth=2)
sns.lineplot(data=season_stats, x='Sezon', y='Rakip Gol', marker='o', color='red', label='Yenilen Gol (Ort)', linewidth=2)
plt.title(f'{team_name} - Sezonlara Göre Gol Ortalamaları', fontsize=13)
plt.ylabel('Gol Ortalaması')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
