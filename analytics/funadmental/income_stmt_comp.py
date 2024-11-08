import yfinance as yf
import pandas as pd
import sqlite3
# Obtener los tickers de las acciones del usuario
tickers = input("Introduce el ticker de la acción que deseas analizar: ").split(',')

# Crear un DataFrame vacío para almacenar los datos financieros
data = {}

# Obtener los datos financieros para cada ticker
for ticker in tickers:
    # Obtener los datos financieros de la acción
    stock = yf.Ticker(ticker)
    income_stmt = stock.financials  # Suponiendo que deseas obtener los estados de ingresos
    # Convertir los datos financieros en un diccionario
    data[ticker] = income_stmt.to_dict()

# Crear DataFrames para cada ticker
dfs = {ticker: pd.DataFrame(data[ticker]) for ticker in data}

# Obtener la intersección de los índices de los DataFrames
common_index = set.intersection(*(set(df.index) for df in dfs.values()))

# Crear un DataFrame para almacenar las diferencias
df_comper = pd.DataFrame()

# Comparar los DataFrames
if len(dfs) > 1:
    # Obtener el primer DataFrame
    df1 = dfs[tickers[0]]
    # Inicializar el DataFrame de diferencias
    df_comper = pd.DataFrame(index=df1.index)  # Inicializar el DataFrame con los índices de df1
    # Comparar con los demás DataFrames
    for ticker in tickers[1:]:
        df2 = dfs[ticker]
        # Filtrar los índices comunes
        df1_common = df1.loc[df1.index.isin(common_index)]
        df2_common = df2.loc[df2.index.isin(common_index)]
        # Reindexar ambos DataFrames para asegurar que tengan las mismas columnas en el mismo orden
        df2_common = df2_common.reindex(columns=df1_common.columns)
        # Calcular las diferencias entre los DataFrames
        differences = df1_common.subtract(df2_common)
        # Concatenar las diferencias al DataFrame de diferencias
        df_comper = pd.concat([df_comper, differences], axis=1)

print(df_comper)

# Guardar el DataFrame de diferencias en una base de datos SQLite
conn = sqlite3.connect(f'analytics\out\database\{str(tickers)}_differences.db')
df_comper.to_sql('differences', conn, if_exists='replace')




# tickers = input("Introduce el ticker de la acción que deseas analizar: ").split(',')
# data = {}
# for ticker in tickers:
#     stock = yf.Ticker(ticker)
#     income_stmt = stock.financials
#     data[ticker] = income_stmt.to_dict()
# print(data)