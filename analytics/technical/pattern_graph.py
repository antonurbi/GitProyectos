import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import talib as ta
from datetime import datetime
ta.CDLENGULFING
ta.CDL2CROWS
ta.CDL3BLACKCROWS
ta.CDL3INSIDE
ta.CDL3LINESTRIKE
ta.CDL3OUTSIDE
ta.CDL3STARSINSOUTH
ta.CDL3WHITESOLDIERS
ta.CDLADVANCEBLOCK
ta.CDLBELTHOLD
ta.CDLBREAKAWAY
ta.CDLCLOSINGMARUBOZU
ta.CDLCONCEALBABYSWALL
ta.CDLCOUNTERATTACK
ta.CDLGAPSIDESIDEWHITE
ta.CDLGRAVESTONEDOJI
ta.CDLHAMMER
ta.CDLHANGINGMAN
ta.CDLHARAMI
ta.CDLHARAMICROSS
ta.CDLHIGHWAVE
ta.CDLHIKKAKE
ta.CDLHIKKAKEMOD
ta.CDLHOMINGPIGEON
ta.CDLIDENTICAL3CROWS
ta.CDLINNECK
ta.CDLINVERTEDHAMMER
ta.CDLKICKING
ta.CDLKICKINGBYLENGTH
ta.CDLLADDERBOTTOM
ta.CDLLONGLEGGEDDOJI
ta.CDLLONGLINE
ta.CDLMARUBOZU
ta.CDLMATCHINGLOW
ta.CDLONNECK
ta.CDLPIERCING
ta.CDLRICKSHAWMAN
ta.CDLRISEFALL3METHODS
ta.CDLSEPARATINGLINES
ta.CDLSHOOTINGSTAR
ta.CDLSHORTLINE
ta.CDLSPINNINGTOP
ta.CDLSTALLEDPATTERN
ta.CDLSTICKSANDWICH
ta.CDLTAKURI
ta.CDLTASUKIGAP
ta.CDLTHRUSTING
ta.CDLTRISTAR
ta.CDLUNIQUE3RIVER
ta.CDLUPSIDEGAP2CROWS
ta.CDLXSIDEGAP3METHODS
ta.CDLABANDONEDBABY
ta.CDLDARKCLOUDCOVER
ta.CDLEVENINGDOJISTAR
ta.CDLEVENINGSTAR
ta.CDLMATHOLD
ta.CDLMORNINGDOJISTAR
ta.CDLMORNINGSTAR


symbol = input('Ingrese el símbolo de la acción: ')
data = yf.download(symbol, period='1mo',  interval='1h')
data_with_patterns = data.copy()
pattern_list = ['ENGULFING', '2CROWS', '3BLACKCROWS', '3INSIDE', '3LINESTRIKE', '3OUTSIDE', '3STARSINSOUTH', '3WHITESOLDIERS', 'ADVANCEBLOCK', 'BELTHOLD', 'BREAKAWAY', 'CLOSINGMARUBOZU', 'CONCEALBABYSWALL', 'COUNTERATTACK', 'GAPSIDESIDEWHITE', 'GRAVESTONEDOJI', 'HAMMER', 'HANGINGMAN', 'HARAMI', 'HARAMICROSS', 'HIGHWAVE', 'HIKKAKE', 'HIKKAKEMOD', 'HOMINGPIGEON', 'IDENTICAL3CROWS', 'INNECK', 'INVERTEDHAMMER', 'KICKING', 'KICKINGBYLENGTH', 'LADDERBOTTOM', 'LONGLEGGEDDOJI', 'LONGLINE', 'MARUBOZU', 'MATCHINGLOW', 'ONNECK', 'PIERCING', 'RICKSHAWMAN', 'RISEFALL3METHODS', 'SEPARATINGLINES', 'SHOOTINGSTAR', 'SHORTLINE', 'SPINNINGTOP', 'STALLEDPATTERN', 'STICKSANDWICH', 'TAKURI', 'TASUKIGAP', 'THRUSTING', 'TRISTAR', 'UNIQUE3RIVER', 'UPSIDEGAP2CROWS', 'XSIDEGAP3METHODS', 'ABANDONEDBABY', 'DARKCLOUDCOVER', 'EVENINGDOJISTAR', 'EVENINGSTAR', 'MATHOLD', 'MORNINGDOJISTAR', 'MORNINGSTAR']

for pattern in pattern_list:
    data_with_patterns[f'CDL{pattern}'] = getattr(ta, f'CDL{pattern}')(data['Open'], data['High'], data['Low'], data['Close'])
pattern_frequency = {}
for pattern in pattern_list:
    pattern_count = data_with_patterns[f'CDL{pattern}'].abs().sum()
    pattern_frequency[pattern] = pattern_count

# Evaluar el rendimiento de cada patrón en los períodos siguientes (por ejemplo, retorno promedio en los siguientes 5 días)
pattern_returns = {}
for pattern in pattern_list:
    signal = data_with_patterns[f'CDL{pattern}']
    next_5_days_returns = data['Close'].pct_change(periods=5).shift(-5)
    pattern_returns[pattern] = next_5_days_returns[signal != 0].mean()

# Seleccionar los 10 patrones más frecuentes que también tienen un buen rendimiento en los períodos siguientes
top_10_patterns = sorted(pattern_frequency, key=lambda x: pattern_frequency[x], reverse=True)[:10]
selected_patterns = sorted(top_10_patterns, key=lambda x: pattern_returns[x], reverse=True)[:10]

fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(20, 10))
colors = mpf.make_marketcolors(up='#a83232', down='#32a88d')
mpl_style = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=colors)
mpf.plot(data, type='candle', ax=axs[0], style=mpl_style)
for pattern in selected_patterns:
    axs[1].plot(data_with_patterns[f'CDL{pattern}'], label=pattern)
axs[1].set_title('Candlestick Patterns')
axs[1].legend(loc='upper left')
plt.show()
print("Los 10 patrones seleccionados basados en su frecuencia y rendimiento futuro son:")
for pattern in selected_patterns:
    print(pattern)