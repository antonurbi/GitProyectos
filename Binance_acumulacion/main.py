import data
import rendimiento
from binance import Client


symbol = 'NEIROUSDT'
interval = Client.KLINE_INTERVAL_1DAY
lookback = '30 day ago UTC'
dias = 1 # Días entre inversiones
inversion = 100 # Cantidad a invertir cada 30 días
# data.get_data(symbol, interval, lookback)
rendimiento.rendimiento(inversion,symbol,inversion, dias)