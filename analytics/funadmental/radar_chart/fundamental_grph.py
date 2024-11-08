import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import mplcursors

def fetch_data_m(tickers):
    # Definir el orden deseado de las columnas
    column_order = [
        'Ticker', 'Total Revenue', 'Operating Revenue', 'Gross Profit', 'Cost Of Revenue', 'Reconciled Cost Of Revenue',
        'Operating Income', 'Net Income', 'EBITDA', 'EBIT', 'Normalized EBITDA', 'Net Income Continuous Operations', 'Pretax Income', 'Tax Provision', 'Net Income From Continuing Operation Net Minority Interest', 'Normalized Income', 'Net Income From Continuing And Discontinued Operation',
        'Total Expenses', 'Operating Expense', 'Interest Expense', 'Interest Expense Non Operating', 'Reconciled Depreciation', 'Research And Development', 'Selling General And Administration',
        'Net Interest Income', 'Interest Income', 'Interest Income Non Operating', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net Non Operating Interest Income Expense', 'Tax Rate For Calcs',
        'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders'
    ]
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        financials =stock.quarterly_financials.transpose()  # Transponer para que las fechas sean filas
        financials['Ticker'] = ticker

        # Asegurarse de que todas las columnas deseadas existan en el DataFrame, inicializar con NaN si falta alguna
        for col in column_order:
            if col not in financials.columns:
                financials[col] = np.nan

        # Reordenar las columnas según el orden definido
        financials = financials[column_order]
        data[ticker] = financials

    combined_df = pd.concat(data.values())
    #print(combined_df.head())
    return combined_df
def fetch_data_y(tickers):
    # Definir el orden deseado de las columnas
    column_order = [
        'Ticker', 'Total Revenue', 'Operating Revenue', 'Gross Profit', 'Cost Of Revenue', 'Reconciled Cost Of Revenue',
        'Operating Income', 'Net Income', 'EBITDA', 'EBIT', 'Normalized EBITDA', 'Net Income Continuous Operations', 'Pretax Income', 'Tax Provision', 'Net Income From Continuing Operation Net Minority Interest', 'Normalized Income', 'Net Income From Continuing And Discontinued Operation',
        'Total Expenses', 'Operating Expense', 'Interest Expense', 'Interest Expense Non Operating', 'Reconciled Depreciation', 'Research And Development', 'Selling General And Administration',
        'Net Interest Income', 'Interest Income', 'Interest Income Non Operating', 'Other Income Expense', 'Other Non Operating Income Expenses', 'Net Non Operating Interest Income Expense', 'Tax Rate For Calcs',
        'Diluted Average Shares', 'Basic Average Shares', 'Diluted EPS', 'Basic EPS', 'Diluted NI Availto Com Stockholders', 'Net Income Common Stockholders'
    ]
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        financials =stock.financials.transpose()  # Transponer para que las fechas sean filas
        financials['Ticker'] = ticker

        # Asegurarse de que todas las columnas deseadas existan en el DataFrame, inicializar con NaN si falta alguna
        for col in column_order:
            if col not in financials.columns:
                financials[col] = np.nan

        # Reordenar las columnas según el orden definido
        financials = financials[column_order]
        data[ticker] = financials

    combined_df = pd.concat(data.values())
    #print(combined_df.head())
    return combined_df
def normalize_and_aggregate_y(df):
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
def normalize_and_aggregate_m(df):
    # Normaliza las métricas financieras a mil millones (1e9)
    # Asumimos que las columnas métricas financieras son todas excepto 'Ticker'
    financial_metrics = [col for col in df.columns if col != 'Ticker' and df[col].dtype in ['float64', 'int64']]
    df[financial_metrics] = df[financial_metrics] / 1e9

    # Agrupa los datos por Ticker, año y mes
    aggregated_data = {}
    for ticker in df['Ticker'].unique():
        ticker_data = df[df['Ticker'] == ticker]
        aggregated_data[ticker] = {}
        for (year, month), group in ticker_data.groupby([ticker_data.index.year, ticker_data.index.month]):
            month_key = f"{year}-{month:02d}"  # Formato del año y mes, ej. '2023-01'
            aggregated_data[ticker][month_key] = group.to_dict()  # Convertir grupo a lista de diccionarios

    return aggregated_data
def plot_multiyear_radar_chart(data, ticker, normalize,time,pt):
    if pt.capitalize() == 'S':
        categories = {
            'Revenue and Cost Metrics': (0, 4),
            'Profitability and Income Metrics': (5, 15),
            'Expense Metrics': (16, 22),
            'Interest and Other Income/Expense Metrics': (23, 29),
            'Shares and Earnings Per Share (EPS) Metrics': (30, 35)
        }

        category_colors = {
            'Revenue and Cost Metrics': 'blue',
            'Profitability and Income Metrics': 'green',
            'Expense Metrics': 'red',
            'Interest and Other Income/Expense Metrics': 'purple',
            'Shares and Earnings Per Share (EPS) Metrics': 'orange'
        }
    else:
        categories = {
            'Métricas de Ingresos': (0,1),
            'Métricas de Costos y Beneficios': (2,4),
            'Métricas de Ingresos y Operaciones': (5,10),
            'Métricas de Impuestos y Patrimonio': (11,15),
            'Gastos y Otras Métricas Operacionales': (16,20),
            'Gastos en Investigación, Desarrollo y Administrativos': (21,22),
            'Ingresos por Actividades Financieras': (23,29),
            'Acciones y Ganancias por Acción (EPS)': (30,35)
        }
        
        category_colors = {
            'Métricas de Ingresos': 'blue',
            'Métricas de Costos y Beneficios': 'green',
            'Métricas de Ingresos y Operaciones': 'black',
            'Métricas de Impuestos y Patrimonio': 'purple',
            'Gastos y Otras Métricas Operacionales': 'orange',
            'Gastos en Investigación, Desarrollo y Administrativos': 'brown',
            'Ingresos por Actividades Financieras': 'red',
            'Acciones y Ganancias por Acción (EPS)': 'gray'
        }
    years = sorted(data.keys())

    num_vars = len(data[next(iter(data))]) - 1

    angles = np.linspace(0,2* np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Completa el círculo

    fig, ax = plt.subplots(figsize=(20, 14), subplot_kw=dict(polar=True), dpi=100)
    colors = plt.cm.plasma(np.linspace(0, 1, len(years)))  # Cambio de esquema de color para mejor diferenciación
    font_size = 10  # Tamaño de fuente fijo para las etiquetas
    font_scale = 0.05  # Factor de escala para convertir longitud de etiqueta en unidades radiales
    for i, year in enumerate(years):
        yearly_data = {k: v for k, v in data[year].items() if k != 'Ticker'}
        values = [list(metric.values())[0] if isinstance(metric, dict) and metric.values() else 0 for metric in yearly_data.values()]
        cleaned_values = [x if isinstance(x, (int, float)) and np.isfinite(x) else 0 for x in values]
        try:
            largo = int(math.log10(cleaned_values[0]) ) -1
        except:
            largo = 6
        eps_indices = [32,33]
        tax_rate_index = 29
        for index in eps_indices:
            cleaned_values[index] *= math.pow(10, largo)

        # Aplicar escala a 'Tax Rate For Calcs'
        cleaned_values[tax_rate_index] *= math.pow(10, largo)
        if normalize:
            # Calcula el valor máximo de los valores limpiados
            max_value = max(cleaned_values) if cleaned_values else 1
            
            # Verifica si el valor máximo es 0 para evitar división por cero
            if max_value == 0:
                values_to_plot = [0 for x in cleaned_values] + [0]
                vales = ['0.00%' for x in values_to_plot]
            else:
                values_to_plot = [(x / max_value) * 100 for x in cleaned_values] + [cleaned_values[0] / max_value * 100]
                vales = [f'{x:.2f}%' for x in values_to_plot]
            max_values_to_plot = max(cleaned_values + [cleaned_values[0]])
        else:
            values_to_plot = cleaned_values + [cleaned_values[0]]
            vales = [f'{x:.2f}' for x in cleaned_values]
        label = f'{ticker} {year}' + (" (Current)" if year == max(years) else "")
        linewidth = 2 if year == max(years) else 1.5
        ax.plot(angles, values_to_plot, 'o-', linewidth=linewidth, label=label, color=colors[i])
        ax.fill(angles, values_to_plot, alpha=0.5, color=colors[i])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    # Configuración de etiquetas con colores de categoría
    count=0
    labels = [k for k in data[next(iter(data))].keys() if k != 'Ticker']
    for label, angle in zip(labels, angles[:-1]):
        alignment = 'left' if 0 < angle < np.pi else 'right'
        if angle == 0 or angle == np.pi:
            alignment = 'center'
        radial_distance = 1.15
        label_length = len(label)
        text = label
        label=text.split(' ')
        if len(label) >= 3:
            label_length = len(label[0]+label[1]+label[2])
        label = ' '.join(label)

        rotation = np.degrees(angle)
        if np.pi / 2 < angle < 3 * np.pi / 2:
            rotation += 180

        # Color por categoría
        for category, (start, end) in categories.items():
            if start <= labels.index(label) <= end:
                color = category_colors[category]
                break
        else:
            color = 'black'  # Color predeterminado si no entra en ninguna categoría
        label = label.split(' ')
        insert = 0
        for i in range(len(label)):
            if i==3 or i==6 :
                label.insert(i, '\n')
                insert+=1
        label = ' '.join(label)
        label= label +'\n'+vales[count]
        if insert <=1:
            font_scale = 0.025
        if np.pi / 2 < angle <= np.pi or 3 * np.pi / 2 <= angle <= 2 * np.pi:
            radial_distance += label_length * font_scale  # Aumenta la distancia en función del tamaño del texto
        count+=1
        if time.capitalize() == 'T':
            if normalize:
                ax.text(angle, radial_distance * 80, label, size=font_size, rotation=rotation,
                        rotation_mode='anchor', horizontalalignment=alignment, verticalalignment='center', color=color)
            else:
                ax.text(angle, radial_distance * max(values_to_plot) , label, size=font_size, rotation=rotation,
                        rotation_mode='anchor', horizontalalignment=alignment, verticalalignment='center', color=color)
        else:
            if normalize:
                ax.text(angle, radial_distance * 80, label, size=font_size, rotation=rotation,
                        rotation_mode='anchor', horizontalalignment=alignment, verticalalignment='center', color=color)
            else:
                ax.text(angle, radial_distance * max(values_to_plot)*0.9, label, size=font_size, rotation=rotation,
                        rotation_mode='anchor', horizontalalignment=alignment, verticalalignment='center', color=color)
    # Agregar leyenda para categorías
    for category, color in category_colors.items():
        ax.plot([], [], color=color, label=category)
    
    
    cursor = mplcursors.cursor(ax, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        index = int(sel.target.index)  # Asegurarse de que el índice es un entero
        sel.annotation.set(
            text=f'{labels[index]}: {values_to_plot[index]:.2f}', 
            fontsize=10, 
            backgroundcolor='white', 
            color='black', 
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightgrey", alpha=0.7)
        )

    selected_points = []

    def on_click(event):
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
            selected_points.append((x, y))
            if len(selected_points) == 2:
                line = plt.Line2D((selected_points[0][0], selected_points[1][0]), (selected_points[0][1], selected_points[1][1]), 
                                color="red", linestyle="--", linewidth=2)
                ax.add_line(line)
                fig.canvas.draw()
                if normalize:
                    diff = np.sqrt((selected_points[0][0] - selected_points[1][0])**2 + (selected_points[0][1] - selected_points[1][1])**2)
                    print(max_values_to_plot)
                    print(diff)
                    diff = (diff * max_values_to_plot) / 100
                    formatted_diff = f'{diff:,.2f}'
                    print(f'Distancia entre los puntos seleccionados: {formatted_diff}')
                else:
                    diff = np.sqrt((selected_points[0][0] - selected_points[1][0])**2 + (selected_points[0][1] - selected_points[1][1])**2)
                    formatted_diff = f'{diff:,.2f}'
                    print(f'Distancia entre los puntos seleccionados: {formatted_diff}')
                # Limpiar los puntos seleccionados
                selected_points.clear()

    fig.canvas.mpl_connect('button_press_event', on_click)
    manager = plt.get_current_fig_manager()     
    manager.toolbar.zoom()
    plt.legend(loc='upper left', bbox_to_anchor=(1.2, 1.05), fontsize='small')
    plt.title(f'{ticker}', size=20, color='darkblue', weight='bold', loc='left')
    # plt.savefig(rf'analytics\out\radar\{ticker}_radar_chart.png')
    plt.show()

def main():
    tickers = ['crm']
    time = input('¿Trimestrales o Anuales? (T/A): ')
    pt= input('¿simple o extendido? (S/Ej):')
    normalize=input('¿Ntormalizar los datos? (Y/N): ')
    if normalize.capitalize() == 'Y':
       normalize = True
    else:
        normalize = False
    if time.capitalize() == 'T':
        fetch_data = fetch_data_m(tickers)
        aggregated_data = normalize_and_aggregate_m(fetch_data)
    if time.capitalize() == 'A':
        fetch_data = fetch_data_y(tickers)
        aggregated_data = normalize_and_aggregate_y(fetch_data)
    for ticker, data in aggregated_data.items():
        plot_multiyear_radar_chart(data, ticker, normalize,time,pt)

if __name__=='__main__':
    main()