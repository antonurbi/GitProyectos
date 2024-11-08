import os
import json
import logging
import time
import pandas as pd
from tqdm import tqdm
import yfinance as yf
import alpaca_trade_api as tradeapi

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LIVE_API_KEY = 'PKYERH84FOA17FBGWFDO'
LIVE_API_SECRET = 'bQfiBhVJXVsfqi00RQT63UFJ7FDEAOB0YNnIlyuP'
LIVE_BASE_URL = 'https://paper-api.alpaca.markets/v2'

def get_active_assets():
    api = tradeapi.REST(LIVE_API_KEY, LIVE_API_SECRET, LIVE_BASE_URL, api_version='v2')
    assets = api.list_assets()
    assets_dict = {}
    for asset in assets:
        if asset.status == 'active':
            assets_dict[asset.symbol] = asset.name
    return assets_dict

def save_fundamental_data(symbols=None):
    """
    Incrementally save fundamental data for a list of stock symbols to CSV files.
    Prioritizes saving data for symbols not already present in the file before updating existing entries.

    Args:
        symbols (list, optional): List of stock symbols. Defaults to None, meaning it will fetch active assets.

    Returns:
        None
    """
    existing_symbols = set()
    download_failures = []

    if symbols is None:
        symbols = list(get_active_assets().keys())
        symbols = [s.replace('.', '-') for s in symbols]

    # Check for existing CSV files
    for symbol in symbols:
        if os.path.exists(f'analytics/fundamental/alpaca/{symbol}.csv'):
            existing_symbols.add(symbol)

    # Separate symbols into those that need to be added and those that need updating
    symbols_to_add = [symbol for symbol in symbols if symbol not in existing_symbols]
    symbols_to_update = [symbol for symbol in symbols if symbol in existing_symbols]

    # Download and save data for symbols not already in CSV files
    download_and_save_symbols(symbols_to_add, download_failures, "Adding new symbols")

    # Update data for symbols already in CSV files
    download_and_save_symbols(symbols_to_update, download_failures, "Updating existing symbols")

    if download_failures:
        logging.info(f"Failed to download data for the following symbols: {', '.join(download_failures)}")
    logging.info("All fundamental data processing attempted.")

def download_and_save_symbols(symbols, download_failures, description):
    """
    Helper function to download and save fundamental data for a list of symbols.

    Args:
        symbols (list): List of symbols to process.
        download_failures (list): List to track symbols that failed to download.
        description (str): Description of the current process phase.

    Returns:
        None
    """
    max_retries = 5
    retry_delay = 5

    for symbol in tqdm(symbols, desc="Processing symbols"):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            # Special handling for 'companyOfficers' column if it's causing serialization issues
            if 'companyOfficers' in info and isinstance(info['companyOfficers'], (list, dict)):
                info['companyOfficers'] = json.dumps(info['companyOfficers'])

            info_df = pd.DataFrame([info])

            if '52WeekChange' in info_df.columns:
                info_df = info_df.rename(columns={'52WeekChange': 'WeekChange_52'})
            if 'yield' in info_df.columns:
                info_df = info_df.rename(columns={'yield': 'yield_value'})

            # Save the DataFrame to a CSV file
            info_df.to_csv(f'analytics/fundamental/alpaca/{symbol}.csv', index=False)
            logging.info(f"Fundamental data saved for {symbol}")

        except Exception as e:
            logging.warning(f"Failed to download data for {symbol}: {e}")
            download_failures.append(symbol)
            continue  # Skip to the next symbol

def print_fundamental_data():
    """
    Access and print the fundamental data for a given stock symbol from a CSV file,
    ensuring all rows are displayed.

    Returns:
    None, but prints the fundamental data for the specified symbol if available.
    """
    symbol = input("Enter the symbol for which you want to view fundamental data: ").strip().upper()
    csv_file_path = f'analytics/fundamental/alpaca/{symbol}.csv'

    if os.path.exists(csv_file_path):
        try:
            data_df = pd.read_csv(csv_file_path)

            # Transpose the DataFrame to print all rows without abbreviation
            data_df_transposed = data_df.T

            # Print all columns without asking for user input
            print(f"Fundamental data for {symbol}:")
            print(data_df_transposed)
        except Exception as e:
            logging.error(f"Error reading CSV file for {symbol}: {e}")
    else:
        logging.info(f"No data found for symbol: {symbol}")

# Ejemplo de uso
symbols = ['AAPL', 'MSFT']
save_fundamental_data(symbols)
print_fundamental_data()
