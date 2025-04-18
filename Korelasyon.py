import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

team_name = "Liverpool"

df = pd.read_excel(f"{team_name}.xlsx")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.head(5))

print(f"\nVeri seti boyutu: {df.shape}")

# ***** Korelasyon Analizi *****

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (14, 10)
sns.set_palette("husl")

df['Sonuç Kategori'] = df['Sonuç'].map({1: 'Galibiyet', 0: 'Beraberlik', -1: 'Mağlubiyet'})

# 1. İsabetli Şut - Gol İlişkisi
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
corr1 = df['İsabetli Şut'].corr(df['Gol'])
ax = sns.regplot(x='İsabetli Şut', y='Gol', data=df,
                scatter_kws={'alpha': 0.6, 's': 80, 'color': '#3498db'},
                line_kws={'color': '#e74c3c', 'linewidth': 2})
plt.title(f'{team_name} - İsabetli Şut ve Gol İlişkisi', fontsize=12)
plt.xlabel('İsabetli Şut Sayısı', fontsize=11)
plt.ylabel('Gol Sayısı', fontsize=11)
plt.grid(True, alpha=0.3)
plt.text(0.05, 0.95, f'Korelasyon: {corr1:.2f}', transform=ax.transAxes,
         fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5, boxstyle='round'))

# 2. Topla Oynama - Sonuç İlişkisi
plt.subplot(2, 2, 2)

corr_possession_result = df['Topla Oynama(%)'].corr(df['Sonuç'].astype(float))

ax = sns.regplot(x='Topla Oynama(%)', y='Sonuç', data=df,
                scatter_kws={'alpha': 0.6, 's': 80, 'color': '#9b59b6'},
                line_kws={'color':'#e74c3c', 'linewidth': 2},
                x_jitter=0.3, y_jitter=0.15)

plt.title(f'{team_name} - Topla Oynama ve Sonuç İlişkisi ', fontsize=12)
plt.xlabel('Topla Oynama Yüzdesi (%)', fontsize=11)
plt.ylabel('Maç Sonucu', fontsize=11)
plt.yticks([-1, 0, 1], ['Mağlubiyet', 'Beraberlik', 'Galibiyet'])
plt.grid(True, alpha=0.3)

plt.text(0.05, 0.95, f'Korelasyon: {corr_possession_result:.2f}',
         transform=ax.transAxes, fontsize=12,
         bbox=dict(facecolor='yellow', alpha=0.5, boxstyle='round'))

# 3.Ofsayt - Rakip Gol İlişkisi
plt.subplot(2, 2, 3)
corr3 = df['Rakip Ofsayt'].corr(df['Rakip Gol'])
ax = sns.regplot(x='Rakip Ofsayt', y='Rakip Gol', data=df,
                scatter_kws={'alpha': 0.6, 's': 80, 'color': '#9b59b6'},
                line_kws={'color': '#e74c3c', 'linewidth': 2})
plt.title(f'{team_name} - Ofsayt ve Rakip Gol İlişkisi', fontsize=12)
plt.xlabel('Rakibin Ofsayta Düşme Sayısı', fontsize=11)
plt.ylabel(f'{team_name} - Yediği Gol Sayısı', fontsize=11)
plt.grid(True, alpha=0.3)
plt.text(0.05, 0.95, f'Korelasyon: {corr3:.2f}', transform=ax.transAxes,
         fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5, boxstyle='round'))

# 4. Pas Başarısı - Topla Oynama İlişkisi
plt.subplot(2, 2, 4)
corr4 = df['Pas Başarısı(%)'].corr(df['Topla Oynama(%)'])
ax = sns.regplot(x='Pas Başarısı(%)', y='Topla Oynama(%)', data=df,
                scatter_kws={'alpha': 0.6, 's': 80, 'color': '#2ecc71'},
                line_kws={'color': '#e74c3c', 'linewidth': 2})
plt.title(f'{team_name} - Pas Başarısı ve Top Hakimiyeti İlişkisi', fontsize=12)
plt.xlabel('Pas Başarısı (%)', fontsize=11)
plt.ylabel('Topla Oynama (%)', fontsize=11)
plt.grid(True, alpha=0.3)
plt.text(0.05, 0.95, f'Korelasyon: {corr4:.2f}', transform=ax.transAxes,
         fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5, boxstyle='round'))

plt.tight_layout()
plt.show()

# İstatistiksel Sonuçlar
print("\n===== Korelasyon Analizi Sonuçları =====")
print("1. İsabetli Şut - Gol: 0.58 (Orta-Güçlü Pozitif)")
print("2. Ofsayt - Rakip Gol: 0.01 (Çok Zayıf)")
print("3. Pas Başarısı - Topla Oynama: 0.56 (Orta-Güçlü Pozitif)")

# Topla Oynama İstatistikleri
print("\n===== Sonuca Göre Topla Oynama Ortalamaları =====")
print(df.groupby('Sonuç Kategori')['Topla Oynama(%)'].mean().round(2))


# Korelasyon Matrisi

exclude_columns = ['Tarih', 'Rakip Takım', 'Takım ID', 'Sezon', 'Ay', 'Haftanın Günü']

numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
selected_cols = [col for col in numeric_cols if col not in exclude_columns]

correlation_df = df[selected_cols]

corr_matrix = correlation_df.corr()

plt.figure(figsize=(16, 12))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title(f"{team_name} - Korelasyon Matrisi", fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
