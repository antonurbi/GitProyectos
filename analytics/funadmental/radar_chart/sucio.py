import yfinance as yf
import pandas as pd
import numpy as np

# Paso 1: Obtener la lista de todas las acciones del Nasdaq
nasdaq_tickers = pd.read_csv('analytics/funadmental/radar_chart/nasdaq-listed-symbols.csv')

# Paso 2: Obtener datos históricos de todas las acciones del Nasdaq
def get_stock_data(tickers):
    stock_data = {}
    for ticker in tickers:
        try:
            stock_data[ticker] = yf.download(ticker, period="1mo", interval="1d")
        except:
            print(f"Could not download data for {ticker}")
    return stock_data

# Limitar a un subconjunto de acciones para reducir el tiempo de ejecución
subset_tickers = nasdaq_tickers['Symbol'].head(100).tolist()
stock_data = get_stock_data(subset_tickers)

# Paso 3: Limpieza de datos
def clean_stock_data(data):
    cleaned_data = {}
    for ticker, df in data.items():
        df.dropna(inplace=True)
        if not df.empty:
            cleaned_data[ticker] = df
    return cleaned_data

cleaned_stock_data = clean_stock_data(stock_data)

# Paso 4: Análisis de datos para encontrar las mejores oportunidades de trading
def calculate_weekly_returns(data):
    weekly_returns = {}
    for ticker, df in data.items():
        df['Weekly Return'] = df['Close'].pct_change(periods=5)
        weekly_returns[ticker] = df['Weekly Return'].iloc[-1]  # Return of the last week
    return weekly_returns

weekly_returns = calculate_weekly_returns(cleaned_stock_data)

# Paso 5: Selección de las mejores acciones
def select_top_stocks(returns, top_n=10):
    sorted_returns = sorted(returns.items(), key=lambda x: x[1], reverse=True)
    return sorted_returns[:top_n]

top_stocks = select_top_stocks(weekly_returns)

print("Top stocks for the week:")
for ticker, ret in top_stocks:
    print(f"{ticker}: {ret:.2%}")

# Paso 6: Visualización de resultados (opcional)
import matplotlib.pyplot as plt

def plot_top_stocks(stocks, data):
    for ticker, _ in stocks:
        data[ticker]['Close'].plot(label=ticker)
    plt.legend()
    plt.title("Top Stocks for the Week")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.show()

plot_top_stocks(top_stocks, cleaned_stock_data)
