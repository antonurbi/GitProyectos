import pandas as pd
import yfinance as yf
from fundamentals import (FinancialAnalysis, ProfitabilityMetrics, CashFlowMetrics, 
                          LiquidityAndEfficiencyMetrics, DebtAndInterestMetrics, 
                          TaxationAndMinorityInterestMetrics, EPSShareMetrics, SpecialItemsMetrics)
import sqlite3 as sql
import matplotlib.pyplot as plt
from math import pi
import numpy as np
def obtener_datos_financieros(tickers):
    financial_data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            income_stmt = stock.financials.T
            if income_stmt.empty:
                raise ValueError(f"No data found for {ticker}")
            income_stmt['Ticker'] = ticker
            financial_data.append(income_stmt)
        except Exception as e:
            print(f"Failed   to fetch data for {ticker}: {e}")
    return financial_data

def create_final_dataframe(results, columns_of_interest):
    final_results = {}
    for ticker, data in results.items():
        # Crear un diccionario para almacenar los datos de interés del ticker actual
        selected_data = {}
        for column in columns_of_interest:
            # Verificar si la columna existe en los datos
            if column in data:
                selected_data[column] = data[column]
            else:
                print(f"Column {column} not found for {ticker}.")
        # Almacenar los datos seleccionados para este ticker en el resultado final
        final_results[ticker] = selected_data
    return final_results
   
def extract_and_normalize(data):
    normalized_data = {}
    for ticker, indicators in data.items():
        ticker_data = {}
        for indicator, series in indicators.items():
            most_recent_value = series.iloc[0]  # Asume que el valor más reciente está al inicio
            if pd.isnull(most_recent_value):
                continue  # Salta indicadores con valores nulos
            
            # Normalización basada en la interpretación específica de cada tipo de indicador
            if 'Margin' in indicator or 'Ratio' in indicator or 'Rate' in indicator or 'Percentage' in indicator:
                # Convierte los valores que son esencialmente porcentuales a una escala de 0 a 1
                if most_recent_value > 1:  # Asume que los valores mayores que 1 están en escala de 100
                    normalized_value = most_recent_value / 100
                else:
                    normalized_value = most_recent_value
            elif 'Trend' in indicator:
                # Los valores de tendencia pueden ser tratados de manera diferente si es necesario
                normalized_value = most_recent_value  # Ajusta según sea necesario
            elif 'EPS' in indicator or 'Profit' in indicator or 'Income' in indicator or 'Expenses' in indicator:
                # Normaliza grandes cifras financieras por mil millones
                normalized_value = most_recent_value / 1e9
            elif 'Impact' in indicator or 'Unusual' in indicator:
                # Trata los impactos y elementos inusuales adecuadamente
                normalized_value = most_recent_value / 1e6  # Por ejemplo, normaliza por millones
            else:
                # Por defecto, asume que el valor ya está en un formato adecuado o requiere un tratamiento especial
                normalized_value = most_recent_value

            ticker_data[indicator] = normalized_value
        normalized_data[ticker] = ticker_data
    return normalized_data

def aggregate_metrics(normalized_data, groups):
    aggregated_data = {}
    for ticker, metrics in normalized_data.items():
        group_values = {}
        for group_name, indicators in groups.items():
            group_metrics = [metrics[ind] for ind in indicators if ind in metrics and not pd.isnull(metrics[ind])]
            if group_metrics:
                # Calculate the average value for the group
                group_values[group_name] = np.mean(group_metrics)
        aggregated_data[ticker] = group_values
    return aggregated_data

def plot_radar_chart(data, ticker):
    labels = list(data.keys())
    num_vars = len(labels)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Complete the loop
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    values = list(data.values()) + [data[labels[0]]]  # Complete the loop
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=ticker)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, rotation=45)
    plt.title(ticker, size=20, color='blue', y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig(rf'analytics\\technical\outputs\radar\{ticker}_radar_chart.png')

tickers = ['CRM']
financial_data = obtener_datos_financieros(tickers)
results={}
# Loop through each ticker's data
for idx, ticker in enumerate(tickers):
    # Get the DataFrame for the current ticker from financial_data list
    data_for_ticker = financial_data[idx]  # Access the DataFrame directly by index

    # Instances of analysis classes
    financial_analysis = FinancialAnalysis(data_for_ticker)
    financial_analysis.calculate_metrics()
    financial_analysis.analyze_growth()
    financial_analysis.categorize_performance()
    
    profitability_metrics = ProfitabilityMetrics(data_for_ticker)
    profitability_metrics.calculate_metrics()
    profitability_metrics.analyze_trends()
    
    cash_flow_metrics = CashFlowMetrics(data_for_ticker)
    cash_flow_metrics.analyze_non_operating_income_expenses()
    cash_flow_metrics.calculate_free_cash_flow()
    cash_flow_metrics.cash_flow_analysis()
    cash_flow_metrics.categorize_performance()
    
    liquidity_and_efficiency_metrics = LiquidityAndEfficiencyMetrics(data_for_ticker)
    liquidity_and_efficiency_metrics.calculate_ratios()
    liquidity_and_efficiency_metrics.analyze_trends()
    liquidity_and_efficiency_metrics.categorize_performance()
    
    debt_and_interest_metrics = DebtAndInterestMetrics(data_for_ticker)
    debt_and_interest_metrics.calculate_ratios()
    debt_and_interest_metrics.analyze_trends()
    debt_and_interest_metrics.categorize_performance()
    
    taxation_and_minority_interest_metrics = TaxationAndMinorityInterestMetrics(data_for_ticker)
    taxation_and_minority_interest_metrics.calculate_indicators()
    taxation_and_minority_interest_metrics.analyze_trends()
    taxation_and_minority_interest_metrics.categorize_performance()
    
    eps_share_metrics = EPSShareMetrics(data_for_ticker)
    eps_share_metrics.calculate_eps()
    eps_share_metrics.analyze_trends()
    eps_share_metrics.dilution_analysis()
    eps_share_metrics.categorize_performance()
    
    special_items_metrics = SpecialItemsMetrics(data_for_ticker)
    special_items_metrics.categorize_items()
    special_items_metrics.analyze_individual_impact()
    special_items_metrics.trend_analysis()
    eps_share_metrics.categorize_performance()
    results[ticker] = data_for_ticker

columns_of_interest = [
    'Gross Profit', 'Gross Profit Margin', 'Operating Expense Ratio', 
    'Total Revenue Growth Rate', 'Operating Revenue Growth Rate', 'Performance Category', 
    'Operating Margin', 'EBITDA Margin', 'Net Profit Margin', 'Operating Income Trend', 
    'EBITDA Trend', 'Net Income Trend', 'Profitability Category', 'Non Operating Impact', 
    'Free Cash Flow', 'Cash Flow Stability', 'Cash Flow Category', 'R&D to Revenue Ratio', 
    'SG&A to Revenue Ratio', 'Operating Expense Ratio', 'Expense to Revenue Ratio', 
    'R&D to Revenue Ratio Trend', 'SG&A to Revenue Ratio Trend', 'Operating Expense Ratio Trend', 
    'Expense to Revenue Ratio Trend', 'Expense Category', 'Interest Coverage Ratio', 
    'Net Interest Margin', 'Interest Coverage Trend', 'Net Interest Margin Trend', 
    'Interest Coverage Category', 'Net Interest Margin Category', 'Effective Tax Rate (ETR)', 
    'Minority Interest Percentage', 'ETR Category', 'Minority Interest Category', 'Basic EPS', 
    'Diluted EPS', 'Basic EPS Trend', 'Diluted EPS Trend', 'Dilution Impact', 
    'Percentage of Dilution', 'EPS Performance Category', 'Unusual Expenses', 'Unusual Incomes', 
    'Impact on Net Income', 'Percentage of Net Income', 'Frequency of Unusual Items', 
    'Direction of Impact', 'Normalized Earnings'
]

# Group the columns by category
category_groups = [
    ['Gross Profit', 'Gross Profit Margin'],
    ['Operating Expense Ratio'],
    ['Total Revenue Growth Rate', 'Operating Revenue Growth Rate'],
    ['Operating Margin', 'EBITDA Margin', 'Net Profit Margin', 'Operating Income Trend', 'EBITDA Trend', 'Net Income Trend'],
    ['Non Operating Impact'],
    ['Free Cash Flow', 'Cash Flow Stability'],
    ['R&D to Revenue Ratio', 'SG&A to Revenue Ratio', 'Operating Expense Ratio', 'Expense to Revenue Ratio', 'R&D to Revenue Ratio Trend', 'SG&A to Revenue Ratio Trend', 'Operating Expense Ratio Trend', 'Expense to Revenue Ratio Trend'],
    ['Interest Coverage Ratio', 'Net Interest Margin', 'Interest Coverage Trend', 'Net Interest Margin Trend'],
    ['Effective Tax Rate (ETR)', 'Minority Interest Percentage'],
    ['Basic EPS', 'Diluted EPS', 'Basic EPS Trend', 'Diluted EPS Trend', 'Dilution Impact', 'Percentage of Dilution'],
    ['Unusual Expenses', 'Unusual Incomes', 'Impact on Net Income', 'Percentage of Net Income', 'Frequency of Unusual Items', 'Normalized Earnings']
]

# Sort the columns of interest based on the category groups
sorted_columns_of_interest = []
for group in category_groups:
    sorted_columns_of_interest.extend(group)

# Update the columns of interest with the sorted list
columns_of_interest = sorted_columns_of_interest

final_data = create_final_dataframe(results, columns_of_interest)  
normalized_data = extract_and_normalize(final_data)
groups = {
    'Profitability and Performance': [
        'Gross Profit', 'Gross Profit Margin', 'Net Profit Margin', 
        'Operating Margin', 'EBITDA Margin', 
        'Operating Income Trend', 'EBITDA Trend', 'Net Income Trend', 
        'Cash Flow Stability'
    ],
    'Revenue and Expense Efficiency': [
        'Total Revenue Growth Rate', 'Operating Revenue Growth Rate', 
        'SG&A to Revenue Ratio', 'R&D to Revenue Ratio', 'Expense to Revenue Ratio', 
        'SG&A to Revenue Ratio Trend', 'R&D to Revenue Ratio Trend', 
        'Operating Expense Ratio Trend', 'Expense to Revenue Ratio Trend'
    ],
    'Financial Health and Capital Structure': [
        'Interest Coverage Ratio', 'Net Interest Margin', 
        'Interest Coverage Trend', 'Net Interest Margin Trend', 

    ],
    'Taxation and Minority Interests': [
        'Effective Tax Rate (ETR)', 'Minority Interest Percentage', 

    ],
    'Earnings Quality and Unusual Items': [
        'Basic EPS', 'Diluted EPS', 'Normalized Earnings', 
        'Dilution Impact', 'Percentage of Dilution', 'Unusual Expenses', 
        'Unusual Incomes', 'Impact on Net Income', 'Percentage of Net Income', 
        'Frequency of Unusual Items', 'Direction of Impact', 'Basic EPS Trend', 
        'Diluted EPS Trend'
    ]
}

aggregated_data = aggregate_metrics(normalized_data, groups)

# Plot radar chart for each company
for ticker in aggregated_data:
    plot_radar_chart(aggregated_data[ticker], ticker)
print('All analysis completed!')




# con = sql.connect('analytics\out\database\fundamental_analysis2.db')
# for ticker, data in final_data.items():
#     df = pd.DataFrame(data)
#     df.to_sql(ticker, con, if_exists='replace')