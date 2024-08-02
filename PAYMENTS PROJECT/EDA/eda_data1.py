import numpy as np 
import pandas as pd 
from ydata_profiling import ProfileReport
import os

# Ruta al archivo CSV
path = r'C:\Users\Onofre\Documents\IRONHACK\DataScience\PAYMENTS PROJECT\project_dataset\extract - cash request - data analyst.csv'

# Cargar los datos
train = pd.read_csv(path, delimiter = ",")

# Generar el informe de perfilado
profile = ProfileReport(train, title = "Profiling Cash Request")

# Ruta para guardar el informe HTML
output_path = os.path.join(os.path.dirname(path), "profiling_cash.html")

# Guardar el informe como un archivo HTML
profile.to_file(output_path)

print(f'Informe de perfilado guardado en: {output_path}')
