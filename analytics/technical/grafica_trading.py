import pandas as pd
import talib
from scipy.signal import find_peaks
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import yfinance as yf
from openai import OpenAI

def fd(ticker):
    stock = yf.Ticker(ticker)
    info = stock.income_stmt
    return info
def calculate_atr(data, atr_period=14):
    """Calcula el ATR (Average True Range) utilizando TA-Lib."""
    high = data['High'].values
    low = data['Low'].values
    close = data['Close'].values
    atr = talib.ATR(high, low, close, timeperiod=atr_period)
    return atr
def find_support_resistance_levels(data):
    """
    Encuentra los niveles de soporte y resistencia basados en la volatilidad del precio.

    :param data: DataFrame con las columnas 'Close', 'High', y 'Low'.
    :return: Tuple de arrays con los niveles de soporte y resistencia.
    """
    # Calcular el ATR como medida de la volatilidad
    atr = talib.ATR(data['High'].values, data['Low'].values, data['Close'].values, timeperiod=20)
    
    # Determinar una distancia mínima para los picos basada en el ATR
    # Podrías ajustar este factor según tus necesidades
    atr_factor = 1.5  # Este factor es ajustable según cómo de sensible quieres que sea la detección de picos
    mean_atr = np.mean(atr)
    min_distance = int((mean_atr / atr_factor) if mean_atr > 0 else 1)
    
    # Encontrar picos y valles usando la distancia mínima calculada
    peaks, _ = find_peaks(data['Close'].values, distance=min_distance)
    troughs, _ = find_peaks(-data['Close'].values, distance=min_distance)
    
    # Extraer los niveles de soporte y resistencia a partir de los picos y valles encontrados
    support_levels = data['Close'].iloc[troughs]
    resistance_levels = data['Close'].iloc[peaks]

    return support_levels.values, resistance_levels.values
def penetration_signal(data, support_levels, resistance_levels, atr_multiplier=1.5, confirmation_bars=2):
    atr = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=14)
    volume = data['Volume']
    ma_short = talib.SMA(data['Close'], timeperiod=20)
    ma_long = talib.SMA(data['Close'], timeperiod=50)
    
    signals = pd.Series(0, index=data.index)
    
    for level in resistance_levels:
        for i in range(len(data)):
            if i < confirmation_bars:  # Skip early data points
                continue
            if data['Close'].iloc[i] > level + atr_multiplier * atr.iloc[i] and \
               data['Volume'].iloc[i] > volume.iloc[i-confirmation_bars:i].mean() and \
               ma_short.iloc[i] > ma_long.iloc[i]:  # Confirm with volume and trend
                signals.iloc[i] = 1  # Buy signal
                
    for level in support_levels:
        for i in range(len(data)):
            if i < confirmation_bars:
                continue
            if data['Close'].iloc[i] < level - atr_multiplier * atr.iloc[i] and \
               data['Volume'].iloc[i] > volume.iloc[i-confirmation_bars:i].mean() and \
               ma_short.iloc[i] < ma_long.iloc[i]:  # Confirm with volume and trend
                signals.iloc[i] = -1  # Sell signal
                
    # Filtrar señales consecutivas iguales
    signals = signals[signals != signals.shift(1)]
    
    return signals

def filter_signals_with_cooldown(signals, cooldown_period=5):
    """
    Filtra señales para introducir un periodo de enfriamiento después de cada señal.
    
    :param signals: Serie de Pandas con señales de trading.
    :param cooldown_period: Número de días de enfriamiento después de cada señal.
    :return: Serie de Pandas con las señales filtradas.
    """
    filtered_signals = signals.copy()
    cooldown = 0
    
    for i in range(1, len(filtered_signals)):
        if cooldown > 0:
            filtered_signals.iloc[i] = 0
            cooldown -= 1
        elif filtered_signals.iloc[i] != 0:
            cooldown = cooldown_period
    
    return filtered_signals

def evaluate_performance(data, signals):
    """
    Evalúa el rendimiento de una estrategia de trading basada en señales de compra/venta.
    
    :param data: DataFrame con los datos históricos de precios.
    :param signals: Serie de Pandas con las señales de trading, 1 para compra, -1 para venta, y 0 para ninguna señal.
    :return: Serie de Pandas con los retornos acumulados de la estrategia.
    """
    # Calcular los retornos diarios del activo
    data['Returns'] = data['Close'].pct_change()
    
    # Alinear las señales con el índice de 'data' para asegurar la correspondencia
    aligned_signals = signals.reindex(data.index, fill_value=0)
    
    # Calcular los retornos de la estrategia
    data['Strategy'] = data['Returns'] * aligned_signals.shift(1)
    data['Strategy'].replace([np.inf, -np.inf], np.nan, inplace=True)
    data['Strategy'].fillna(0, inplace=True)
    # Calcular los retornos acumulados de la estrategia
    cumulative_returns = (1 + data['Strategy']).cumprod()
    
    return cumulative_returns

def analyze_trades_performance(trades):
    """
    Analiza el rendimiento de las operaciones de trading.

    :param trades: DataFrame con las operaciones, incluyendo precios de entrada y salida.
    :return: Diccionario con el análisis de rendimiento.
    """
    if trades.empty:
        print("No hay operaciones para analizar.")
        return {}

    # Asumiendo que 'trades' ya incluye una columna 'return' calculada previamente
    total_return = trades['return'].sum()
    positive_trades = trades[trades['return'] > 0]
    negative_trades = trades[trades['return'] <= 0]
    win_rate = len(positive_trades) / len(trades) if len(trades) > 0 else 0
    avg_win = positive_trades['return'].mean() if not positive_trades.empty else 0
    avg_loss = negative_trades['return'].mean() if not negative_trades.empty else 0
    profit_factor = abs(positive_trades['return'].sum() / negative_trades['return'].sum()) if not negative_trades.empty else np.inf

    # Cálculo del drawdown máximo
    cumulative_returns = (1 + trades['return']).cumprod() - 1
    max_drawdown = (cumulative_returns.cummax() - cumulative_returns).max()

    # Cálculo del ratio de Sharpe, asumiendo tasa libre de riesgo = 0 para simplificar
    sharpe_ratio = trades['return'].mean() / trades['return'].std() if trades['return'].std() != 0 else np.inf

    performance_summary = {
        'total_return': total_return,
        'win_rate': win_rate,
        'average_win': avg_win,
        'average_loss': avg_loss,
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio
    }

    # Imprimir el resumen del análisis de rendimiento
    for key, value in performance_summary.items():
        if key in ['total_return', 'win_rate', 'average_win', 'average_loss', 'max_drawdown']:
            print(f"{key.replace('_', ' ').capitalize()}: {value:.2%}")
        else:
            print(f"{key.replace('_', ' ').capitalize()}: {value:.2f}")

    return performance_summary

def generate_trades_from_signals(data, signals):
    """
    Genera un DataFrame de operaciones a partir de las señales de trading.
    
    :param data: DataFrame con los datos históricos de precios.
    :param signals: Serie de Pandas con las señales de trading. El índice es DateTimeIndex y los valores son 1 (compra), -1 (venta) y 0 (ninguna señal).
    :return: DataFrame de operaciones realizadas que incluye fechas de entrada y salida, y el retorno de cada operación.
    """
    trades = []
    entry_price = None
    entry_date = None
    
    for date, signal in signals.items():
        if signal > 0 and entry_price is None:  # Señal de compra
            entry_price = data.loc[date, 'Close']
            entry_date = date
        elif signal < 0 and entry_price is not None:  # Señal de venta
            exit_price = data.loc[date, 'Close']
            returns = (exit_price - entry_price) / entry_price
            trades.append({'entry_date': entry_date, 'exit_date': date, 'return': returns})
            entry_price = None  # Reset para la próxima operación
    
    # Crear un DataFrame a partir de la lista de trades
    trades_info = pd.DataFrame(trades)
    
    return trades_info

def download_data(symbol, period):
    """
    Descarga datos históricos del símbolo dado para el período especificado desde Yahoo Finance y limpia los datos.
    
    :param symbol: Símbolo del instrumento financiero (por ejemplo, '^DJI').
    :param period: Período para el cual se descargarán los datos (por ejemplo, '2y' para 2 años).
    :return: DataFrame de Pandas con los datos históricos limpios.
    """
    try:
        # Descargar datos usando yfinance
        data = yf.download(symbol, period=period)
        
        # Convertir el índice a datetime sin zona horaria si es necesario
        data.index = data.index.tz_localize(None)
        
        # Seleccionar solo las columnas relevantes
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        # Asegurar que todos los datos son flotantes
        data = data.astype(float)
    except Exception as e:
        print(f"Error al descargar los datos para el símbolo {symbol}: {e}")
        data = pd.DataFrame()
    
    return data

def find_important_levels(levels, num_levels=2):
    """
    Identifica los niveles más importantes de soporte o resistencia.

    :param levels: Array de niveles de soporte o resistencia.
    :param num_levels: Número de niveles importantes a devolver.
    :return: Array con los niveles más importantes.
    """
    # Contar cuántas veces aparece cada nivel
    level_counts = {level: list(levels).count(level) for level in set(levels)}
    
    # Ordenar los niveles por frecuencia de aparición
    sorted_levels = sorted(level_counts.items(), key=lambda item: item[1], reverse=True)
    
    # Tomar los 'num_levels' más frecuentes
    important_levels = [level for level in sorted_levels[:num_levels]]
    
    return important_levels

def rw_top(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index < order * 2 + 1:
        return False

    top = True
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] > v or data[k - i] > v:
            top = False
            break
    
    return top

def rw_bottom(data: np.array, curr_index: int, order: int) -> bool:
    if curr_index < order * 2 + 1:
        return False

    bottom = True
    k = curr_index - order
    v = data[k]
    for i in range(1, order + 1):
        if data[k + i] < v or data[k - i] < v:
            bottom = False
            break
    
    return bottom

def rw_extremes(data: np.array, order:int):
    # Rolling window local tops and bottoms
    tops = []
    bottoms = []
    for i in range(len(data)):
        if rw_top(data, i, order):
            # top[0] = confirmation index
            # top[1] = index of top
            # top[2] = price of top
            top = [i, i - order, data[i - order]]
            tops.append(top)
        
        if rw_bottom(data, i, order):
            # bottom[0] = confirmation index
            # bottom[1] = index of bottom
            # bottom[2] = price of bottom
            bottom = [i, i - order, data[i - order]]
            bottoms.append(bottom)
    
    return tops, bottoms

def draw_trendlines(data,tops, bottoms, ax, idx):
    # Configuración para la validación de líneas de tendencia
    min_distance = 20  # Distancia mínima en índices entre puntos

    # Draw resistance lines
    for i in range(len(tops)):
        for j in range(i+1, len(tops)):
            if abs(tops[j][1] - tops[i][1]) < min_distance:
                continue  # Verificar la distancia entre puntos
            if tops[i][2] < tops[j][2]:
                continue  # Asegurar que la segunda cima sea menor que la primera
            # Verificar que no corte a través del precio
            if not any(tops[i][2] >= data['Close'][tops[i][1]:tops[j][1]]):
                ax.plot([idx[tops[i][1]], idx[tops[j][1]]], [tops[i][2], tops[j][2]], 'g--')

    # Draw support lines
    for i in range(len(bottoms)):
        for j in range(i+1, len(bottoms)):
            if abs(bottoms[j][1] - bottoms[i][1]) < min_distance:
                continue  # Verificar la distancia entre puntos
            if bottoms[i][2] > bottoms[j][2]:
                continue  # Asegurar que el segundo mínimo sea mayor que el primero
            # Verificar que no corte a través del precio
            if not any(bottoms[i][2] <= data['Close'][bottoms[i][1]:bottoms[j][1]]):
                ax.plot([idx[bottoms[i][1]], idx[bottoms[j][1]]], [bottoms[i][2], bottoms[j][2]], 'r--')

def plot_support_resistance_levels(data, important_support_levels, important_resistance_levels, filtered_signals, performance_summary, symbol,code):
    info = fd(symbol)
    print(info)
    # Filter the data for the last 5 years
    end_date = data.index.max()  # Latest date in your dataset
    start_date = end_date - pd.DateOffset(years=5)  # 5 years before the end date
    data_5_years = data.loc[start_date:end_date]

    # Assuming rw_extremes and draw_trendlines are functions defined previously
    tops, bottoms = rw_extremes(data_5_years['Close'].to_numpy(), 10)
    idx = data_5_years.index
    plt.figure(figsize=(14, 7), dpi=100)

    # Assuming draw_trendlines is a function defined previously
    draw_trendlines(data_5_years, tops, bottoms, plt, idx)
    plt.plot(data_5_years['Close'], label='Precio de Cierre', alpha=1.0, linewidth=2, color='blue')
    ymin, ymax = data_5_years['Close'].min(), data_5_years['Close'].max()
    margin = (ymax - ymin) * 0.1
    plt.ylim(ymin - margin, ymax + margin)
    xmin, xmax = idx.min(), idx.max()

    for level in important_support_levels:
        plt.hlines(level, xmin=xmin, xmax=xmax, color='green', linestyle='--',
                   label='Soporte Importante' if 'Soporte Importante' not in plt.gca().get_legend_handles_labels()[1] else "")

    for level in important_resistance_levels:
        plt.hlines(level, xmin=xmin, xmax=xmax, color='red', linestyle='--',
                   label='Resistencia Importante' if 'Resistencia Importante' not in plt.gca().get_legend_handles_labels()[1] else "")

    # Align signals with the data index
    buy_signals = filtered_signals[filtered_signals > 0]
    sell_signals = filtered_signals[filtered_signals < 0]
    aligned_buy_signals = buy_signals[buy_signals.index.isin(data_5_years.index)]
    aligned_sell_signals = sell_signals[sell_signals.index.isin(data_5_years.index)]

    plt.scatter(aligned_buy_signals.index, data_5_years['Close'][aligned_buy_signals.index], label='Compra', color='green', marker='^', s=100)
    plt.scatter(aligned_sell_signals.index, data_5_years['Close'][aligned_sell_signals.index], label='Venta', color='red', marker='v', s=100)

    plt.title(f'Precio de Cierre y Rendimiento Acumulado con Señales de Trading para {symbol}')
    plt.xlabel('Fecha')
    plt.ylabel('Precio / Rendimiento Acumulado')
    plt.legend()
    if code == 'averse': 
        plt.savefig(fr'analytics\out\resistences\averse\{symbol}_averse.png')
    elif code == 'taker':
        plt.savefig(fr'analytics\out\resistences\taker\{symbol}_taker.png')
    elif code == 'other':
        plt.savefig(fr'analytics\out\resistences\other\{symbol}_other.png')
    
    plt.figure(figsize=(17,17), dpi=100) 
    ax = plt.gca()
    ax.axis('off')
    tbl = ax.table(cellText=info.values, colLabels=info.columns, rowLabels=info.index, loc='center', cellLoc='center', colLoc='center', colColours=['#f4f4f4']*len(info.columns), colWidths=[0.1]*len(info.columns))
    # Ajustar el tamaño de la tabla
    tbl.auto_set_column_width([i for i in range(len(info.columns))])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(0.75, 2)  
    
    if code == 'averse':
        plt.savefig(fr'analytics\out\fundamental\averse\{symbol}_averse_info.png')
    elif code == 'taker':
        plt.savefig(fr'analytics\out\fundamental\taker\{symbol}_taker_info.png')
    elif code == 'other':
        plt.savefig(fr'analytics\out\fundamental\other\{symbol}_other_info.png')
    print("\nResumen del Rendimiento de las Operaciones:")
    for key, value in performance_summary.items():
        print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")


def support_resistance_levels_data(symbol, period):
    
        # Cargar datos
    data = download_data(symbol, period)
    
    # Asegurar que todos los datos son flotantes
    data = data.astype(float)
    
    # Encontrar niveles de soporte y resistencia
    support_levels, resistance_levels = find_support_resistance_levels(data)
    
    # Generar señales de trading basadas en la penetración de los niveles de S/R
    signals = penetration_signal(data, support_levels, resistance_levels)
    
    # Incorporar un periodo de enfriamiento o confirmación para las señales
    cooldown_period = 5  # Días de enfriamiento después de cada señal
    filtered_signals = filter_signals_with_cooldown(signals, cooldown_period)
    
    # Generar un DataFrame de operaciones basadas en las señales filtradas
    trades_info = generate_trades_from_signals(data, filtered_signals)
    
    # Evaluar el rendimiento de la estrategia
    cumulative_returns = evaluate_performance(data, filtered_signals)
    
    # Analizar el rendimiento de las operaciones
    performance_summary = analyze_trades_performance(trades_info)
    important_support_levels = find_important_levels(support_levels)
    important_resistance_levels = find_important_levels(resistance_levels)
    
    return data, important_support_levels, important_resistance_levels, filtered_signals, performance_summary
def optimizer_sr_levels(support_levels, num_bins=20, use_median=True, top_n_bins=8):
    """
    Optimiza los niveles de soporte, encontrando los más comunes.

    :param support_levels: Diccionario con intervalos como claves y listas de niveles de soporte como valores.
    :param num_bins: Número de bins a usar en el histograma para agrupar niveles de soporte.
    :param use_median: Booleano para decidir si usar la mediana o la media para representar el nivel importante.
    :param top_n_bins: Número de bins más comunes a considerar para encontrar niveles importantes.
    :return: Lista de niveles de soporte importantes.
    """
    # Aplanar la lista de todos los niveles de soporte
    all_levels = [level for sublist in support_levels.values() for level in sublist]
    
    # Convertir a un array de numpy para facilitar el análisis
    levels_array = np.array(all_levels)
    
    # Determinar los rangos de precios (bins) para agrupar los niveles de soporte
    min_level = levels_array.min()
    max_level = levels_array.max()
    bins = np.linspace(min_level, max_level, num=num_bins)
    
    # Histograma para encontrar los rangos de precios más comunes
    histogram, bins = np.histogram(levels_array, bins=bins)
    
    # Tomar los top_n_bins rangos más comunes
    most_common_bins_indices = np.argsort(histogram)[-top_n_bins:]
    most_common_bins = []

    for idx in most_common_bins_indices:
        # Asegúrese de que el índice no sea el último, lo cual no tendría un par correspondiente en 'bins'
        if idx < len(bins)-1:
            bin_range = (bins[idx], bins[idx + 1])
            most_common_bins.append(bin_range)
    
    # Encontrar los niveles de soporte importantes dentro de los rangos más comunes
    important_levels = []
    for bin_min, bin_max in most_common_bins:
        # Filtrar los niveles dentro de este rango
        important_levels_in_bin = levels_array[(levels_array >= bin_min) & (levels_array <= bin_max)]
        # Tomar la mediana o media de estos niveles como el nivel importante
        if important_levels_in_bin.size > 0:
            if use_median:
                important_level = np.median(important_levels_in_bin)
            else:
                important_level = np.mean(important_levels_in_bin)
            # Añadir el nivel a la lista si no es igual a 1
            if important_level != 1:
                important_levels.append(important_level)
    
    return important_levels
def optimizer_filtered_signals(filtered_signals):

    """
    Optimiza las señales filtradas identificando las más consistentes a través de diferentes intervalos.

    :param filtered_signals: Diccionario con intervalos como claves y Series de pandas con señales filtradas como valores.
    :return: Series de pandas consolidada con señales optimizadas.
    """
    consolidated_buy_signals = pd.Series(dtype='int64')
    consolidated_sell_signals = pd.Series(dtype='int64')
    
    # Consolidar señales de compra y venta por separado
    for interval, signals in filtered_signals.items():
        buy_signals = signals[signals > 0]
        sell_signals = signals[signals < 0]
        
        consolidated_buy_signals = consolidated_buy_signals.add(buy_signals, fill_value=0)
        consolidated_sell_signals = consolidated_sell_signals.add(sell_signals, fill_value=0)
    
    # Normalizar señales: 1 para compra, -1 para venta, ignorando la magnitud de la señal original
    consolidated_buy_signals[consolidated_buy_signals > 0] = 1
    consolidated_sell_signals[consolidated_sell_signals < 0] = -1
    
    # Combinar señales de compra y venta en una sola Serie
    optimized_signals = consolidated_buy_signals.add(consolidated_sell_signals, fill_value=0)
    
    # Filtrar señales optimizadas para mantener solo aquellas con suficiente respaldo a través de los intervalos
    # Este paso puede ajustarse según el criterio específico, como un umbral de frecuencia mínima
    optimized_signals = optimized_signals[optimized_signals != 0]
    
    return optimized_signals


def inicializar_cliente_openai(api_key):
    return OpenAI(api_key=api_key)
def openai_respuesta(performance_summary, symbol):
    
    api_key= "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"
    client=inicializar_cliente_openai(api_key)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Este es un sistema diseñado para proporcionar análisis detallado fundamental para trading."},
            {"role": "user", "content": performance_summary},
            {"role": "user", "content": f"Evalua el rendimiento de la estrategia de trading para el símbolo {symbol}, y."},
        ],
        model="gpt-4",
        max_tokens=500
    )
    return chat_completion.choices[0].message.content.strip()

def consolidate_performance_summary(performance_summary):
    info = pd.DataFrame.from_dict(performance_summary, orient='index')
    info.replace([np.inf, -np.inf], np.nan, inplace=True)
    info.fillna(0, inplace=True)
    info['gain_to_loss_ratio'] = info.apply(lambda row: row['average_win'] / row['average_loss'] if row['average_loss'] != 0 else np.nan, axis=1)
    info['total_return'] = info['total_return'].apply(lambda x: f"{x:.2%}")
    info['win_rate'] = info['win_rate'].apply(lambda x: f"{x:.2%}")
    info['average_win'] = info['average_win'].apply(lambda x: f"{x:.2%}")
    info['average_loss'] = info['average_loss'].apply(lambda x: f"{x:.2%}")
    info['profit_factor'] = info['profit_factor'].replace(0, np.nan)
    info['max_drawdown'] = info['max_drawdown'].apply(lambda x: f"{x:.2%}")
    info['sharpe_ratio'] = info['sharpe_ratio'].round(2)
    return info
def performance_summary_to_text(info, symbol):
    """
    Convierte un DataFrame de resumen de rendimiento en un texto descriptivo.

    :param info: DataFrame que contiene el resumen de rendimiento.
    :param symbol: El símbolo del activo al que se refiere el rendimiento.
    :return: Una cadena de texto que describe el rendimiento.
    """
    # Inicializar una lista para almacenar las líneas del texto
    lines = [f"Resumen de rendimiento para el símbolo {symbol}:"]
    
    # Iterar sobre cada fila del DataFrame para agregar los detalles al texto
    for index, row in info.iterrows():
        lines.append(f"\nIntervalo: {index}")
        for column, value in row.items():
            # Asegurarse de que los valores NaN se manejen adecuadamente en el texto
            if pd.isna(value):
                value = "N/A"
            lines.append(f"{column}: {value}")
    
    # Unir todas las líneas en una sola cadena de texto
    performance_text = "\n".join(lines)
    
    return performance_text

def sup_resis(symbol,code):
    #symbol = input('Simbolo a graficar: ')  # Símbolo del Dow Jones Industrial Average
    intervals = [ '1mo', '3mo','1y', '2y','4y']
    list_of_support_levels = {}
    list_of_resistance_levels = {}
    list_of_performance_summary = {}
    list_of_filtered_signals = {}
    for interval in intervals:
        print(f"Procesando datos para el intervalo '{interval}'...")
        data,important_support_levels, important_resistance_levels, filtered_signals, performance_summary = support_resistance_levels_data(symbol, interval)
        list_of_support_levels[interval] = important_support_levels
        list_of_resistance_levels[interval] = important_resistance_levels
        list_of_performance_summary[interval] = performance_summary
        list_of_filtered_signals[interval] = filtered_signals
    all_results = {
        'support_levels': list_of_support_levels,
        'resistance_levels': list_of_resistance_levels,
        'performance_summary': list_of_performance_summary,
        'filtered_signals': list_of_filtered_signals
    }
    important_support_levels = optimizer_sr_levels(all_results['support_levels'])
    important_resistance_levels = optimizer_sr_levels(all_results['resistance_levels'])
    filtered_signals = optimizer_filtered_signals(all_results['filtered_signals'])
    performance_summary = consolidate_performance_summary(all_results['performance_summary'])
    plot_support_resistance_levels(data, important_support_levels, important_resistance_levels, filtered_signals, performance_summary, symbol,code)
    # performance_text = performance_summary_to_text(performance_summary, symbol)
    # respuesta= openai_respuesta(performance_text, symbol)
    # print(respuesta)
