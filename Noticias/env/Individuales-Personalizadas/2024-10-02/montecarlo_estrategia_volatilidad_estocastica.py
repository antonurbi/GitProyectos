import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 1. Obtener datos recientes del precio del oro (últimos 2 años)
# Ticker 'GC=F' para futuros del oro
gold = yf.download('GC=F', start='2022-01-01', end=datetime.today())['Adj Close']

# 2. Calcular los retornos logarítmicos diarios
log_returns = np.log(gold / gold.shift(1)).dropna()

# 3. Parámetros iniciales para la simulación Monte Carlo
mu = log_returns.mean()
sigma = log_returns.std()
T = 252  # Días de trading en un año
n_simulations = 10000  # Número de simulaciones
n_days = 252  # Número de días para la simulación (1 año)

# 4. Simulación Monte Carlo del precio del oro
def monte_carlo_simulation(start_price, mu, sigma, n_days, n_simulations):
    simulations = np.zeros((n_days, n_simulations))
    for sim in range(n_simulations):
        prices = [start_price]
        for day in range(1, n_days):
            drift = mu - 0.5 * sigma**2
            shock = sigma * np.random.normal()
            price = prices[-1] * np.exp(drift + shock)
            prices.append(price)
        simulations[:, sim] = prices
    return simulations

def detectar_puntos_de_liquidez(simulated_prices, n_intervals=5, threshold=0.05):
    """
    Detecta puntos de liquidez basados en un histograma de precios simulados.
    
    simulated_prices: Precios simulados de Monte Carlo (matriz de n_días x n_simulaciones)
    n_intervals: Número de momentos en el tiempo que queremos analizar (ej. 5, 10, 30 días).
    threshold: Proporción mínima para considerar un punto como de alta liquidez (ej. 0.05).
    
    Retorna un diccionario con los días analizados y los puntos de precios de alta liquidez.
    """
    n_days, n_simulations = simulated_prices.shape
    points_of_liquidity = {}

    # Dividimos el periodo total en n_intervals
    interval_days = np.linspace(0, n_days-1, n_intervals, dtype=int)

    for day in interval_days:
        # Histograma de los precios simulados en el día específico
        precios_del_dia = simulated_prices[day, :]
        hist, bin_edges = np.histogram(precios_del_dia, bins=50, density=True)
        
        # Determinar puntos de alta liquidez donde la densidad es mayor que el umbral
        puntos_liquidez = bin_edges[:-1][hist > threshold]

        # Guardar los resultados
        points_of_liquidity[day] = puntos_liquidez

        # Graficar el histograma para análisis visual
        plt.figure(figsize=(8, 4))
        plt.hist(precios_del_dia, bins=50, density=True, alpha=0.6, color='g')
        plt.axhline(y=threshold, color='r', linestyle='--', label=f'Umbral de liquidez ({threshold})')
        plt.title(f'Distribución de precios simulados en el día {day}')
        plt.xlabel('Precio del Oro (USD)')
        plt.ylabel('Densidad de precios')
        plt.legend()
        plt.show()
    
    return points_of_liquidity


# 5. Correr la simulación Monte Carlo usando el precio más reciente
start_price = gold.iloc[-1]  # Precio actual
simulated_prices = monte_carlo_simulation(start_price, mu, sigma, n_days, n_simulations)

# 6. Calcular las estadísticas de las simulaciones
final_prices = simulated_prices[-1, :]
mean_final_price = np.mean(final_prices)
std_final_price = np.std(final_prices)

# 7. Graficar los resultados de las simulaciones junto con el precio histórico
plt.figure(figsize=(10,6))

# Graficar el precio histórico del oro
plt.plot(gold.index, gold.values, label='Precio Histórico', color='blue')

# Graficar las simulaciones de Monte Carlo
simulated_dates = [gold.index[-1] + np.timedelta64(i, 'D') for i in range(n_days)]
for i in range(100):  # Graficar solo 100 simulaciones para no sobrecargar la gráfica
    plt.plot(simulated_dates, simulated_prices[:, i], color='grey', alpha=0.1)

plt.title('Simulación Monte Carlo del Precio del Oro (1 año)')
plt.xlabel('Días de trading')
plt.ylabel('Precio del oro (USD)')
plt.legend()
plt.show()

# 8. Imprimir resultados
print(f"Precio actual del oro: {start_price:.2f} USD")
print(f"Precio promedio al final del año (Monte Carlo): {mean_final_price:.2f} USD")
print(f"Desviación estándar de precios simulados: {std_final_price:.2f} USD")

puntos_de_liquidez = detectar_puntos_de_liquidez(simulated_prices, n_intervals=5, threshold=0.05)

# Mostrar los resultados
for day, puntos in puntos_de_liquidez.items():
    print(f"Día {day}: Puntos de liquidez en precios {puntos}")