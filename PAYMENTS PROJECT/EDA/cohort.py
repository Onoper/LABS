import pandas as pd

# Ruta al archivo CSV
path = r'DataScience\PAYMENTS PROJECT\project_dataset\extract - cash request - data analyst.csv'
path2 = r'DataScience\PAYMENTS PROJECT\project_dataset\extract - fees - data analyst - .csv'

# Cargar los datos
df = pd.read_csv(path, delimiter=",")  # cash requests
df2 = pd.read_csv(path2, delimiter=",")  # fees

# Imputación de IDs faltantes (usmos deletec_account_id para reconstruir los ids que nos faltan)
df['user_id'] = df['user_id'].fillna(df['deleted_account_id'])

# Descarte de transacciones canceladas para que no se tengan en cuenta en ninguna variable
df = df[df['status'] != 'canceled']

# Descarte de fees sin cash_request_id






# Construcción de cohortes
df['created_at'] = pd.to_datetime(df['created_at'])  

# Encontrar la fecha de 'created_at' más baja para cada 'user_id' dentro de cada cohorte
first_dates = df.groupby('user_id')['created_at'].min().reset_index()
first_dates.columns = ['user_id', 'activation_date']

# Extraer el mes y año en el formato YY/MM
first_dates['cohorte'] = first_dates['activation_date'].dt.strftime('%y/%m')

# Merge de esta información de vuelta al DataFrame original
df = df.merge(first_dates[['user_id', 'cohorte']], on='user_id', how='left')

# Calcular el tamaño de cada cohorte (número de usuarios únicos)
cohort_sizes = df.groupby('cohorte')['user_id'].nunique().reset_index()
cohort_sizes.columns = ['COHORT', 'COHORT_SIZE']

# Agrupar por cohorte y mes (periodo) y calcular las variables solicitadas
cohort_data = []
for (cohorte, periodo), group in df.groupby(['cohorte', pd.Grouper(key='created_at', freq='ME')]):
    num_transacciones = int(group['id'].nunique())
    num_incidencias = int(group['recovery_status'].notna().sum())  
    # sumamos todas los cash request que tengan informado algun recovery status, ya que los NaN representan transacciones sin incidencias

    
    # Filtrar y sumar el total_amount de df2
    accepted_fees = df2[df2['cash_request_id'].isin(group['id']) & (df2['status'] == 'accepted')]['total_amount'].sum()
    # para calcular los ingresos solo tenemos en cuenta los fees que se han podido cobrar (status==accepted)

    pending_fees = df2[df2['cash_request_id'].isin(group['id']) & (df2['status'].isin(['rejected', 'confirmed']))]['total_amount'].sum()
     # para calcular los ingresos pendientes tenemos en cuenta los fees que no se han podido cobrar (status==rejected+confirmed)

    cohort_size = cohort_sizes[cohort_sizes['COHORT'] == cohorte]['COHORT_SIZE'].values[0]
    # calculamos el tamaño de cada cohorte de acuerdo al numero de usuarios unicos

    incidence_rate = round(num_incidencias / num_transacciones, 2)
    # calculamos la tasa de incidencias dividiendo el numero de incidencias por el numero de transacciones

    transactions_rate = round(num_transacciones/cohort_size,2)
    # calculamos el ratio de transacciones por usuario dividiendo el total de transacciones por el numero de usuarios en la cohorte 

    cohort_data.append({
        'COHORT': cohorte,
        'COHORT_SIZE': cohort_size,
        'PERIOD': periodo.strftime('%Y-%m'),
        'TOTAL_TRANSACTIONS': int(num_transacciones),
        'TRANSACTIONS_RATE': transactions_rate,  
        'TOTAL_INCIDENCES': int(num_incidencias),
        'ACCEPTED_FEES': accepted_fees,  
        'PENDING_FEES': pending_fees,
        'INCIDENCE_RATE': incidence_rate
    })

# Crear el DataFrame final
df_final = pd.DataFrame(cohort_data)

# Guardar DataFrame en CSV
df_final.to_csv(r'DataScience\PAYMENTS PROJECT\EDA\cohort_data.csv', index=False)

