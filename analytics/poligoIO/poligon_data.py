import requests
import pandas as pd

def fetch_ticker_details(api_key, ticker):
    base_url = "https://api.polygon.io"
    
    endpoints = {
        "ticker_details": f"/v3/reference/tickers/{ticker}",
        "ticker_news": f"/v2/reference/news?ticker={ticker}",
        "market_status": "/v1/marketstatus/now",
        "stock_financials": f"/v2/reference/financials/{ticker}",
        "aggregate_bars": f"/v2/aggs/ticker/{ticker}/prev",
        "ticker_events": f"/v1/meta/symbols/{ticker}/company",
        "dividends": f"/v2/reference/dividends/{ticker}",
        "splits": f"/v2/reference/splits/{ticker}"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {}
    for key, endpoint in endpoints.items():
        url = f"{base_url}{endpoint}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data[key] = response.json()
        else:
            data[key] = None
            print(f"Failed to fetch {key}: {response.status_code}")
    
    return data

# Example usage
api_key = "BGiVYym6HzbZFKd6OH69phbfsKvpSZFT"
ticker = "TSLA"
data = fetch_ticker_details(api_key, ticker)

def split_data(data):
    ticker_details = data.get("ticker_details")
    ticker_news = data.get("ticker_news")
    market_status = data.get("market_status")
    stock_financials = data.get("stock_financials")
    aggregate_bars = data.get("aggregate_bars")
    ticker_events = data.get("ticker_events")
    dividends = data.get("dividends")
    splits = data.get("splits")
    
    # Convert JSON data to pandas DataFrames or dictionaries as needed
    if ticker_details:
        ticker_details_df = pd.json_normalize(ticker_details, sep='_')
    else:
        ticker_details_df = pd.DataFrame()

    if ticker_news:
        ticker_news_df = pd.json_normalize(ticker_news['results'], sep='_')
    else:
        ticker_news_df = pd.DataFrame()

    if stock_financials:
        stock_financials_df = pd.json_normalize(stock_financials['results'], sep='_')
    else:
        stock_financials_df = pd.DataFrame()

    if aggregate_bars:
        aggregate_bars_df = pd.json_normalize(aggregate_bars['results'], sep='_')
    else:
        aggregate_bars_df = pd.DataFrame()

    if dividends:
        dividends_df = pd.json_normalize(dividends['results'], sep='_')
    else:
        dividends_df = pd.DataFrame()

    if splits:
        splits_df = pd.json_normalize(splits['results'], sep='_')
    else:
        splits_df = pd.DataFrame()
    
    return {
        "ticker_details": ticker_details_df,
        "ticker_news": ticker_news_df,
        "stock_financials": stock_financials_df,
        "aggregate_bars": aggregate_bars_df,
        "dividends": dividends_df,
        "splits": splits_df
    }

# Example usage
split_data_dict = split_data(data)

split_data_dict.to_csv('analytics/secondtrading/ticker_data.csv', index=False)
