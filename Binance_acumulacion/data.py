from binance import Client
import pandas as pd

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

def getminutdata(symbol, interval, lookback):
    df = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback ))
    df = df.iloc[:, :6]  # Mantener solo las primeras 6 columnas
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']  # Nombres de columnas en mayúsculas

    # Convertir el tiempo a formato datetime
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

    # Formatear el tiempo para que incluya milisegundos y coincida con el formato requerido
    df['datetime'] = df['datetime'].dt.strftime('%d.%m.%Y %H:%M:%S.%f')  # Formato con milisegundos

    # Convertir las columnas numéricas a tipo float
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    return df

def get_data(symbol, interval, lookback):
    # Obtener datos y guardarlos en CSV
    df = getminutdata(symbol, interval, lookback)
    df.to_csv("data.csv", index=True)  # Guardar sin índice
