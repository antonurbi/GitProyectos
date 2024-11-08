import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def fetch_data(tickers):
    # Definir el orden deseado de las columnas
    column_order = [
        'Ticker','Total Revenue', 'Operating Revenue', 'Gross Profit', 'Cost Of Revenue', 'Reconciled Cost Of Revenue',
        'Operating Income', 'Net Income', 'EBITDA', 'EBIT', 'Normalized EBITDA', 'Net Income Continuous Operations', 'Pretax Income', 'Tax Provision', 'Net Income From Continuing Operation Net Minority Interest', 'Normalized Income', 'Net Income From Continuing And Discontinued Operation',
        'Total Expenses', 'Operating Expense', 'Interest Expense', 'Interest Expense Non Operating', 'Reconciled Depreciation', 'Research And Development', 'Selling General And Administration',
        'Net Interest Income', 'Interest Income', 'Interest Income Non Operating', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net Non Operating Interest Income Expense',
        'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders'
    ]
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        financials = stock.financials.transpose()  # Transponer para que las fechas sean filas
        financials['Ticker'] = ticker
        # Reordenar las columnas según el orden definido
        financials = financials.loc[:, column_order]
        data[ticker] = financials
    combined_df = pd.concat(data.values())
    return combined_df

def normalize_and_aggregate(df):
    # Asumiendo que las columnas son métricas y los índices son las fechas (pd.Timestamp)
    large_scale_metrics = [col for col in df.columns if 'EPS' not in col and df[col].dtype != 'object']
    
    # Normaliza las métricas financieras a mil millones (1e9)
    df[large_scale_metrics] = df[large_scale_metrics] / 1e9
    
    # Prepara un diccionario para almacenar los datos agregados por año y por ticker
    aggregated_data = {}
    for ticker in df['Ticker'].unique():
        ticker_data = df[df['Ticker'] == ticker]
        aggregated_data[ticker] = {}
        
        # Agrupar datos por año
        for year, group in ticker_data.groupby(ticker_data.index.year):
            aggregated_data[ticker][year] = group.to_dict()

    return aggregated_data

def plot_multiyear_radar_chart(data, ticker, normalize=False):
    years = sorted(data.keys())
    num_vars = len(data[next(iter(data))]) - 1

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Completa el círculo

    fig, ax = plt.subplots(figsize=(14, 14), subplot_kw=dict(polar=True))
    colors = plt.cm.plasma(np.linspace(0, 1, len(years)))  # Cambio de esquema de color para mejor diferenciación
    font_size = 6.5  # Tamaño de fuente fijo para las etiquetas
    font_scale = 0.013  # Factor de escala para convertir longitud de etiqueta en unidades radiales
    
    for i, year in enumerate(years):
        yearly_data = {k: v for k, v in data[year].items() if k != 'Ticker'}
        values = [list(metric.values())[0] if isinstance(metric, dict) and metric.values() else 0 for metric in yearly_data.values()]
        cleaned_values = [x if isinstance(x, (int, float)) and np.isfinite(x) else 0 for x in values]

        if normalize:
            max_value = max(cleaned_values) if cleaned_values else 1
            values_to_plot = [(x / max_value) * 100 for x in cleaned_values] + [cleaned_values[0] / max_value * 100]
        else:
            values_to_plot = cleaned_values + [cleaned_values[0]]

        label = f'{ticker} {year}' + (" (Current)" if year == max(years) else "")
        linewidth = 3 if year == max(years) else 1.5
        ax.plot(angles, values_to_plot, 'o-', linewidth=linewidth, label=label, color=colors[i])
        ax.fill(angles, values_to_plot, alpha=0.4, color=colors[i])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    labels = [k for k in data[next(iter(data))].keys() if k != 'Ticker']
    for label, angle in zip(labels, angles[:-1]):
        alignment = 'left' if 0 < angle < np.pi else 'right'
        if angle == 0 or angle == np.pi:
            alignment = 'center'
        label_length = len(label)
        text = label
        label=text.split(' ')
        if len(label) >= 3:
            label_length = len(label[0]+label[1]+label[2])
        for i in range(len(label)):
            if i == 3:
                label.insert(i, '\n')   
        label = ' '.join(label)
    
        radial_distance = 1.15 if angle in (0, np.pi) else 1.1
        if angle == 0 or angle == np.pi:
            radial_distance = 1.15

        # Ajusta la distancia radial basada en la longitud de la etiqueta para cuadrantes 2 y 4
        if np.pi / 2 < angle < np.pi or 3 * np.pi / 2 < angle < 2 * np.pi:
            radial_distance += label_length * font_scale  # Aumenta la distancia en función del tamaño del texto

        rotation = np.degrees(angle)
        if np.pi / 2 < angle < 3 * np.pi / 2:
            rotation += 180

        ax.text(angle, radial_distance * max(values_to_plot), label, size=font_size, rotation=rotation,
                rotation_mode='anchor', horizontalalignment=alignment, verticalalignment='center', color='black')

    if normalize:
        plt.title(f'{ticker} N)', size=20, color='darkblue', weight='bold',loc='left')
    else:
        plt.title(f'{ticker}', size=20, color='darkblue', weight='bold',loc='left')
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.05), fontsize='small')
    plt.savefig(f'analytics/out/radar/{ticker}_multiyear_radar_chart.png', bbox_inches='tight')
    plt.show()

# Uso del ejemplo
tickers = ['AAPL']
df = fetch_data(tickers)
aggregated_data = normalize_and_aggregate(df)

for ticker, data in aggregated_data.items():
    plot_multiyear_radar_chart(data, ticker)
