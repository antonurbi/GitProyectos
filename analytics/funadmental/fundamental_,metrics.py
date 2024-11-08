import yfinance as yf
import pandas as pd

# Función para obtener datos financieros con yfinance
def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials.T
    balance_sheet = stock.balance_sheet.T
    cashflow = stock.cashflow.T
    info = stock.info
    
    data = {
        'Ticker': ticker,
        'Total Revenue': financials.loc[:, 'Total Revenue'][0],
        'Operating Income': financials.loc[:, 'Operating Income'][0],
        'Gross Profit': financials.loc[:, 'Gross Profit'][0],
        'Cost Of Revenue': financials.loc[:, 'Cost Of Revenue'][0],
        'Net Income': financials.loc[:, 'Net Income'][0],
        'EBITDA': financials.loc[:, 'EBITDA'][0],
        'Pretax Income': financials.loc[:, 'Pretax Income'][0],
        'Tax Provision': financials.loc[:, 'Income Tax Expense'][0],
        'Total Assets': balance_sheet.loc[:, 'Total Assets'][0],
        'Total Liabilities': balance_sheet.loc[:, 'Total Liabilities'][0],
        'Stockholders Equity': balance_sheet.loc[:, 'Total Stockholder Equity'][0],
        'Current Assets': balance_sheet.loc[:, 'Total Current Assets'][0],
        'Current Liabilities': balance_sheet.loc[:, 'Total Current Liabilities'][0],
        'Inventory': balance_sheet.loc[:, 'Inventory'][0],
        'Cash and Cash Equivalents': balance_sheet.loc[:, 'Cash'][0],
        'Market Capitalization': info['marketCap'],
        'Diluted EPS': info['trailingEps'],
        'Basic EPS': info['trailingEps'],
        'Interest Expense': cashflow.loc[:, 'Interest Paid'][0] * -1,
        'Research And Development': financials.loc[:, 'Research Development'][0],
        'Selling General And Administration': financials.loc[:, 'Selling General Administrative'][0],
    }
    return data

# Obtener datos financieros de ejemplo
ticker = 'AAPL'
data = get_financial_data(ticker)

# Crear DataFrame
df = pd.DataFrame([data])

# Función para generar análisis fundamental
def fundamental_analysis(df):
    analysis = {}
    for _, row in df.iterrows():
        ticker = row['Ticker']
        try:
            analysis[ticker] = {
                # Ratios de Rentabilidad
                'Gross Margin': row['Gross Profit'] / row['Total Revenue'],
                'Operating Margin': row['Operating Income'] / row['Total Revenue'],
                'Net Profit Margin': row['Net Income'] / row['Total Revenue'],
                'Return on Equity (ROE)': row['Net Income'] / row['Stockholders Equity'],
                'Return on Assets (ROA)': row['Net Income'] / row['Total Assets'],
                # Ratios de Liquidez
                'Current Ratio': row['Current Assets'] / row['Current Liabilities'],
                'Quick Ratio': (row['Current Assets'] - row['Inventory']) / row['Current Liabilities'],
                # Ratios de Endeudamiento
                'Debt-to-Equity Ratio': row['Total Liabilities'] / row['Stockholders Equity'],
                'Interest Coverage Ratio': row['Operating Income'] / row['Interest Expense'],
                # Ratios de Eficiencia
                'Asset Turnover': row['Total Revenue'] / row['Total Assets'],
                'Inventory Turnover': row['Cost Of Revenue'] / row['Inventory'],
                # Ratios de Mercado
                'P/E Ratio': row['Market Capitalization'] / row['Net Income'],
                'P/B Ratio': row['Market Capitalization'] / row['Stockholders Equity'],
                # Otros
                'Effective Tax Rate': row['Tax Provision'] / row['Pretax Income'],
                'EBITDA Margin': row['EBITDA'] / row['Total Revenue'],
                'Diluted EPS': row['Diluted EPS'],
                'Basic EPS': row['Basic EPS'],
            }
        except:
            pass
    return analysis

# Generar el análisis
analysis = fundamental_analysis(df)

# Mostrar el análisis con interpretaciones
for ticker, metrics in analysis.items():
    print(f"Análisis fundamental para {ticker}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.2f}")
    # Interpretación básica
    print("\nInterpretaciones:")
    if metrics['Gross Margin'] > 0.4:
        print("  - Alta eficiencia en la producción y venta de productos.")
    if metrics['Net Profit Margin'] > 0.1:
        print("  - La empresa es rentable.")
    if metrics['Current Ratio'] > 1.5:
        print("  - Buena capacidad para cubrir pasivos a corto plazo.")
    if metrics['Quick Ratio'] > 1:
        print("  - Buena liquidez sin depender de inventarios.")
    if metrics['Debt-to-Equity Ratio'] < 1:
        print("  - Baja dependencia de la deuda para financiar sus activos.")
    if metrics['ROE'] > 0.15:
        print("  - Alta eficiencia en la generación de beneficios con el capital propio.")
    if metrics['P/E Ratio'] < 15:
        print("  - La acción puede estar infravalorada.")
    print()
