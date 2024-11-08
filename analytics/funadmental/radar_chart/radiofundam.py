import yfinance as yf
import matplotlib.pyplot as plt
from math import pi
import numpy as np
import pandas as pd

def normalize_and_aggregate(df):
    large_scale_metrics = [col for col in df.columns if 'EPS' not in col and '' not in col and df[col].dtype != 'object']
    df[large_scale_metrics] = df[large_scale_metrics] / 1e9  # Normalize large financial figures
    
    category_groups = {
        'Revenue and Cost Metrics': ['Total Revenue', 'Operating Revenue', 'Gross Profit', 'Cost Of Revenue', 'Reconciled Cost Of Revenue'],
        'Profitability and Income Metrics': ['Operating Income', 'Net Income', 'EBITDA', 'EBIT', 'Normalized EBITDA', 'Net Income Continuous Operations', 'Pretax Income', 'Tax Provision', 'Net Income From Continuing Operation Net Minority Interest', 'Normalized Income', 'Net Income From Continuing And Discontinued Operation'],
        'Expense Metrics': ['Total Expenses', 'Operating Expense', 'Interest Expense', 'Interest Expense Non Operating', 'Reconciled Depreciation', 'Research And Development', 'Selling General And Administration'],
        'Interest and Other Income/Expense Metrics': ['Net Interest Income', 'Interest Income', 'Interest Income Non Operating', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net Non Operating Interest Income Expense'],
        'Shares and Earnings Per Share (EPS) Metrics': ['Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders'],
        
    }
    category_groups = {
        ['Total Revenue', 'Operating Revenue', 'Gross Profit', 'Cost Of Revenue', 'Reconciled Cost Of Revenue',
        'Operating Income', 'Net Income', 'EBITDA', 'EBIT', 'Normalized EBITDA', 'Net Income Continuous Operations', 'Pretax Income', 'Tax Provision', 'Net Income From Continuing Operation Net Minority Interest', 'Normalized Income', 'Net Income From Continuing And Discontinued Operation',
        'Total Expenses', 'Operating Expense', 'Interest Expense', 'Interest Expense Non Operating', 'Reconciled Depreciation', 'Research And Development', 'Selling General And Administration',
        'Net Interest Income', 'Interest Income', 'Interest Income Non Operating', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net Non Operating Interest Income Expense',
        'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders']
        
    }
    aggregated_data = {}
    for ticker in df['Ticker'].unique():
        ticker_data = df[df['Ticker'] == ticker]
        aggregated_data[ticker] = {}
        for category, columns in category_groups.items():
            relevant_columns = [col for col in columns if col in ticker_data.columns]
            aggregated_data[ticker][category] = ticker_data[relevant_columns].mean(axis=1).dropna().mean()

    return aggregated_data

def plot_radar_chart(data, ticker):
    labels = list(data.keys())
    values = [data[key] for key in labels]

    # Número de variables que tenemos
    num_vars = len(labels)

    # Calcula los ángulos de cada eje en el radar
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist() + [0]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Dibuja la línea que rodea el radar
    ax.plot(angles, values + values[:1], linewidth=2, linestyle='solid', label=ticker)
    
    # Rellena el área debajo de la línea
    ax.fill(angles, values + values[:1], alpha=0.25)
    
    # Mejora las etiquetas de los ejes
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=13, rotation=45, ha='right')

    # Ajusta la configuración del título y la leyenda
    plt.title(f'{ticker} Financial Metrics Radar Chart', size=18, color='darkred', weight='bold')
    plt.legend(loc='upper right', fontsize='large')
    
    # Añade una cuadrícula más visible
    ax.grid(True)
    
    plt.savefig(rf'analytics\out\radar\sucio\{ticker}_radar_chart.png')

def fetch_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        # Assuming we are interested in annual financials
        financials = stock.financials.transpose()  # Transpose to make dates as rows
        financials['Ticker'] = ticker
        data[ticker] = financials
    combined_df = pd.concat(data.values())
    return combined_df
# Example usage
df = {}
tickers = ['QUBT', 'IBM', 'ionq']
df = fetch_data(tickers)    
aggregated_data = normalize_and_aggregate(df)
for ticker, data in aggregated_data.items():
    plot_radar_chart(data, ticker)
