import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Ruta al archivo CSV
file_path = r'C:\Users\Onofre\Documents\IRONHACK\DataScience\PAYMENTS PROJECT\EDA\cohort_data.csv'

# Cargar datos desde el archivo CSV
df = pd.read_csv(file_path)

# Ordenar por 'PERIOD' numéricamente
df.sort_values(by='PERIOD', inplace=True)

# Reorganizar los datos para el mapa de calor
# df_heatmap = df.pivot(index='COHORT', columns='PERIOD', values='INCIDENCE_RATE')

# # Crear el mapa de calor
# plt.figure(figsize=(10, 6))
# sns.heatmap(df_heatmap, annot=True, cmap='viridis', fmt='.2f', cbar=True)
# plt.title('Mapa de Calor: Incidencia por Cohorte y Mes (Ordenado)')
# plt.xlabel('Mes')
# plt.ylabel('Cohorte')
# plt.tight_layout()
# plt.show()

# MAPA DE CALOR TRANSACCIONES
# Reorganizar los datos para el mapa de calor
df_heatmap = df.pivot(index='COHORT', columns='PERIOD', values='TOTAL_TRANSACTIONS')
df_heatmap = df_heatmap.fillna(0).astype(int)
# Crear el mapa de calor
plt.figure(figsize=(10, 6))
sns.heatmap(df_heatmap, annot=True, cmap='viridis', fmt='d', cbar=True)
plt.title('Mapa de Calor: Transaciones por Cohorte y Mes (Ordenado)')
plt.xlabel('Mes')
plt.ylabel('Cohorte')
plt.tight_layout()
plt.show()

# Reorganizar los datos para el mapa de calor
# df_heatmap2 = df.pivot(index='COHORT', columns='PERIOD', values='ACCEPTED_FEES')

# # Crear el mapa de calor
# plt.figure(figsize=(10, 6))
# sns.heatmap(df_heatmap2, annot=True, cmap='viridis', fmt='.2f', cbar=True)
# plt.title('Mapa de Calor: Fees por Cohorte y Mes (Ordenado)')
# plt.xlabel('Mes')
# plt.ylabel('Cohorte')
# plt.tight_layout()
# plt.show()