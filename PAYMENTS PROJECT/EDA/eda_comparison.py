import pandas as pd 

# Ruta al archivo CSV
path = r'C:\Users\Onofre\Documents\IRONHACK\DataScience\PAYMENTS PROJECT\project_dataset\extract - cash request - data analyst.csv'
path2 = r'C:\Users\Onofre\Documents\IRONHACK\DataScience\PAYMENTS PROJECT\project_dataset\extract - fees - data analyst - .csv'

# Cargar los datos
df = pd.read_csv(path, delimiter=",")  #cash requests
df2 = pd.read_csv(path2, delimiter=",")  # fees


# print(requests.sort_values(by='id', ascending=False).head(30))
# print(fees.sort_values(by='cash_request_id', ascending=False).head(30))
# value_counts = fees['cash_request_id'].value_counts()
# print(value_counts)


# IMPUTACION IDS FALTANTES

df['user_id'] = df['user_id'].fillna(df['deleted_account_id'])

# CONSTRUCCIÓN DE COHORTES

# Asegúrate de que 'created_at' esté en formato de fecha
df['created_at'] = pd.to_datetime(df['created_at'])

# Encontrar la fecha de 'created_at' más baja para cada 'user_id'
first_dates = df.groupby('user_id')['created_at'].min().reset_index()
first_dates.columns = ['user_id', 'activation_date']

# Extraer el mes y año en el formato MM_YY
first_dates['cohorte'] = first_dates['activation_date'].dt.strftime('%m_%y')

# Mergear esta información de vuelta al DataFrame original
df = df.merge(first_dates[['user_id', 'cohorte']], on='user_id', how='left')

#agrupar y contar el numero de registros por cada cohorte
cohort_counts = df.groupby('cohorte').size().reset_index(name='num_transactions')

# Crear el diccionario de cohortes
cohort_dict = {}

# Agrupar por cohorte y recorrer cada grupo, generando lista de Ids y variables total transacciones, incidencias y el ratio.
for cohorte, group in df.groupby('cohorte'):
    request_ids = group['id'].tolist()
    num_transactions = len(request_ids)
    num_incidencias = group['recovery_status'].notna().sum()  # Contar los valores no NaN en 'recovery_status'
    
    # Filtrar y sumar el total_amount de df2
    total_amount_accepted = df2[df2['cash_request_id'].isin(request_ids) & (df2['status'] == 'accepted')]['total_amount'].sum()
    total_amount_rejected = df2[df2['cash_request_id'].isin(request_ids) & (df2['status'] == 'rejected')]['total_amount'].sum()
    
    cohort_dict[cohorte] = {
        'request_ids': request_ids,
        'num_transacciones': num_transactions,
        'num_incidencias': num_incidencias,
        'tasa_incidencia': round(num_incidencias / num_transactions, 2),
        'total_amount_accepted': total_amount_accepted,
        'total_amount_rejected': total_amount_rejected
    }

# Imprimir los resultados
for cohorte, info in cohort_dict.items():
    print(f"Cohorte: {cohorte}, Num Transacciones: {info['num_transacciones']}, Num Incidencias: {info['num_incidencias']}, Tasa Incidencia: {info['tasa_incidencia']}, Total Amount Accepted: {info['total_amount_accepted']}, Total Amount Rejected: {info['total_amount_rejected']}")