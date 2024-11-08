import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import yfinance as yf
import talib as ta
import mplfinance as mpf
from grafica_trading import sup_resis as sr
import math

#plots
def plot_time_series_with_summary(data, title, x_label, y_label):
    plt.figure(figsize=(16, 10))
    plt.plot(data, '-')
    plt.axhline(y=data.mean(), label='Mean', color='r')
    plt.fill_between(data.index, (data.mean() - data.std()), (data.mean() + data.std()), color='b', alpha=.1,
                     label='Volatility')
    plt.title(title, fontsize=16)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    plt.legend()
    plt.show()    
def visualization_of_stock_data(data_ex):
    plt.style.use('seaborn-v0_8-colorblind')
    plt.figure(figsize=(18, 8), dpi=120, constrained_layout=True)
    plt.plot(data_ex['Adj Close'], '-')
    plt.gcf().autofmt_xdate()
    plt.title('data_ex Stock Price 2005-2024', fontsize=16)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Price in $', fontsize=16)
    plt.show()

#tickers
def get_tickers_data(tickers):
    tickers_data = []
    tickers_prices = {}
    tickers_df = {}
    for ticker in tickers:
        try:
            yf.pdr_override()
            raw_data = pdr.get_data_yahoo(ticker, start="2005-01-01", end="2024-04-20")[['Adj Close']].rename(columns={'Adj Close': 'Price'}).copy()
            raw_data['d+1'] = raw_data['Price'].shift(-1)
            raw_data['ROI'] = np.log(raw_data['d+1'] / raw_data['Price']) * 100
            monthly_price = raw_data.resample('M').last()
            monthly_price['lower'] = monthly_price['ROI'] - monthly_price['ROI'].std()
            monthly_price['upper'] = monthly_price['ROI'] + monthly_price['ROI'].std()
            
            tickers_prices[ticker] = {
                'Expected Return': monthly_price['ROI'].mean(),
                'Risk': monthly_price['ROI'].std(),
                'Data_length': len(monthly_price['ROI']),
                'Data': {
                    'Changes': monthly_price['ROI'].values.tolist(),
                    'Margin of Error': monthly_price[['lower', 'upper']].values.tolist()
                }
            }
            tickers_data.append([ticker, monthly_price['ROI'].mean(), monthly_price['ROI'].std(), len(monthly_price['ROI'])])
            tickers_df[ticker] = monthly_price
        except Exception as e:
            print(e)
            print(ticker)
    return tickers_df, tickers_data
def indonesian_tickers():
    idx_tickers=[f'{idx_tickers}.JK' for idx_tickers in [
        'ACES',
        'EXCL',
        'ITMG',
        'SMGR',
        'ADRO',
        'BBTN',
        'GOTO',
        'JPFA',
        'SRTG',
        'AKRA',
        'BMRI',
        'BRPT',
        'HRUM',
        'KLBF',
        'TBIG',
        'AMRT',
        'BRIS',
        'ICBP',
        'MDKA',
        'TINS',
        'ANTM',
        'BRPT',
        'INCO',
        'MEDC',
        'TLKM',
        'ARTO',
        'AALI',
        'INDF',
        'PGAS',
        'TOWR',
        'ASII',
        'CPIN',
        'INDY',
        'PTBA',
        'TPIA',
        'BBCA',
        'INKP',
        'SCMA',
        'UNTR',
        'BBNI',
        'ESSA',
        'INTP',
        'SIDO',
        'UNVR',
        'BBRI'

    ]]

    tickers=['AAPL','TSLA', 'META', 'AMZN', 'MSFT']+idx_tickers
    return tickers
def ticker_QQQ():
    tickers=[f'{tickers}' for tickers in ['ATVI','ADBE','ALTR','AMZN','APCC','AMGN','APOL','AAPL','AMAT','ATYT','ADSK','BEAS','BBBY','BIIB','BMET','BRCM','CDNS','CDWC','CELG','CHRW','CHKP','CKFR','CHIR','CTAS','CSCO','CTXS','CTSH','CMCSA','CMVT','COST','DELL','XRAY','DISCA','EBAY','DISH','ERTS','EXPE','EXPD','ESRX','FAST','FISV','FLEX','GRMN','GENZ','GILD','GOOG','IACI','INTC','INTU','JDSU','JNPR','KLAC','LRCX','LAMR','LBTYA','LNCR','LLTC','ERICY','META','MRVL','MXIM','MCIP','MEDI','MERQ','MCHP','MSFT','MNST','NTAP','NIHD','NVLS','NTLI','NVDA','ORCL','PCAR','PDCO','PTEN','PAYX','PETM','PIXR','QCOM','RHAT','RIMM','ROST','SNDK','SHLD','SEPR','SEPR','SIRI','SPLS','SBUX','SUNW','SYMC','TSLA','TLAB','TEVA','URBN','VRSN','WFMI','WYNN','XLNX','XMSR','YHOO']]
    return tickers
def ticker_input():
    tickers = input('Enter the tickers split by (,) : ').split(',')
    return tickers


def averge_return(data_ex):
    price_2013=data_ex['Adj Close'][0]
    price_2023=data_ex['Adj Close'][-1]
    roi=np.log(price_2023/price_2013)*100
    print(f'Price on {data_ex.index[0].strftime("%d-%m-%Y")}:  RP {round(price_2013,2)}')
    print(f'Price on {data_ex.index[-1].strftime("%d-%m-%Y")}: RP {round(price_2023,2)}')
    print(f'Return on Investment: {round(roi,2)}%')
    
    #Monthly return
    data_ex['Price d+1']=data_ex['Adj Close'].shift(-1)
    data_ex['ROI']=np.log(data_ex['Price d+1']/data_ex['Adj Close'])*100
    data_ex=data_ex[['ROI']].resample('1M').sum()
    plot_time_series_with_summary(data_ex['ROI'], 'Volatility of data_ex', 'Date', 'ROI in %' )
def crypto_tickers():
    from yahooquery import Screener

    s = Screener()
    data = s.get_screeners('all_cryptocurrencies_us', count=250)
    symbol_list = []
    # data is in the quotes key
    data['all_cryptocurrencies_us']['quotes']
    for symbol in data['all_cryptocurrencies_us']['quotes']:
        symbol_list.append(symbol['symbol'])
    return symbol_list
def Risk_averse(df_tickers_data):
    averse=[]
    other=[]    
    y_mean=df_tickers_data['Risk'].mean()
    x_mean=df_tickers_data['Expected Return'].mean()
    for i in range (len(df_tickers_data)):
        txt=df_tickers_data['Ticker'][i]
        x=df_tickers_data['Expected Return'][i]
        y=df_tickers_data['Risk'][i]
        if y<y_mean and x>x_mean:
            averse.append(txt)
        else:
            other.append(txt)
    return averse,other
def Risk_taker(df_tickers_data):
    taker=[]
    y_mean=df_tickers_data['Risk'].mean()
    x_mean=df_tickers_data['Expected Return'].mean()
    for i in range (len(df_tickers_data)):
        txt=df_tickers_data['Ticker'][i]
        x=df_tickers_data['Expected Return'][i]
        y=df_tickers_data['Risk'][i]
        if y>y_mean and x>x_mean:
            taker.append(txt)
    return taker    
def level_of_volatility(data_ex):
    print('Level of Volatility') 
    mean=data_ex['Adj Close'].mean()
    count=data_ex['Adj Close'].count()
    std=data_ex['Adj Close'].std()
    min=data_ex['Adj Close'].min()
    max=data_ex['Adj Close'].max()
    vola=data_ex['Adj Close'].describe(percentiles=[.25, .5, .75],include='all')
    print(
    f'Mean: {mean}\n'
    f'Count: {count}\n'
    f'Std: {std}\n'
    f'Min: {min}\n'
    f'Max: {max}\n'
    f'Vola: {vola}\n'
    )

def scatter_graph(tickers_data, tickers_df, tickers):
    # Filter tickers list to include only those present in tickers_df
    valid_tickers = [ticker for ticker in tickers if ticker in tickers_df]

    if len(valid_tickers) == 1:
        fig, ax = plt.subplots(figsize=(8, 6))
        ticker = valid_tickers[0]
        data = tickers_df[ticker]['ROI']
        ax.plot(data, '-')
        ax.axhline(y=data.mean(), label='Mean', color='r')
        ax.fill_between(data.index, (data.mean() - data.std()), (data.mean() + data.std()), color='b', alpha=0.1, label='Volatility')
        ax.set_title(f'{ticker} Volatility/Risk')
        ax.legend()
    else:
        num_tickers = len(valid_tickers)
        num_cols = 2
        num_rows = math.ceil(num_tickers / num_cols)
        counter = 0
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 15))
        fig.suptitle('Sample of Stock Volatility/Risk', fontsize=20)
        for i in range(num_rows):
            for j in range(num_cols):
                if counter < num_tickers:
                    ticker = valid_tickers[counter]
                    data = tickers_df[ticker]['ROI']
                    axes[i, j].plot(data, '-')
                    axes[i, j].axhline(y=data.mean(), label='Mean', color='r')
                    axes[i, j].fill_between(data.index, (data.mean() - data.std()), (data.mean() + data.std()), color='b', alpha=0.1, label='Volatility')
                    axes[i, j].set_title(f'{ticker}')
                    counter += 1
                else:
                    # If there are more subplots than tickers, remove the empty subplots
                    fig.delaxes(axes[i, j])

        plt.tight_layout()
        plt.show()

    df_tickers_data = pd.DataFrame(tickers_data, columns=['Ticker', 'Expected Return', 'Risk', 'Data Length'])
    
    plt.style.use('seaborn-v0_8-colorblind')
    plt.figure(figsize=(20,10))
    plt.plot(df_tickers_data['Expected Return'], df_tickers_data['Risk'], '.', markersize=20)
    plt.title('Expected Return VS Risk', fontsize=20)
    for i in range (len(df_tickers_data)):
        txt=df_tickers_data['Ticker'][i]
        x=df_tickers_data['Expected Return'][i]
        y=df_tickers_data['Risk'][i]
        plt.annotate(txt,(x-0.01, y +0.01), fontsize=12)
    plt.axhline(y=df_tickers_data['Risk'].mean(),label= 'Risk Mean', color='r')
    plt.vlines(x=df_tickers_data['Expected Return'].mean(),label='Expected Return Mean', color='y', ymin=(np.min(df_tickers_data['Risk'])), ymax=(np.max(df_tickers_data['Risk'])))
    plt.xlabel('Expected Return', fontsize=16)
    plt.ylabel('Risk', fontsize=16)
    plt.legend()
    plt.savefig('analytics\out\Expected Return VS Risk.png')
    return df_tickers_data
def candlestick_chart(ticker):
    
    ta.CDLENGULFING # Dos velas donde la segunda vela cubre completamente la primera.
    
    ta.CDLHAMMER  #Vela con un cuerpo pequeño en la parte superior y una larga sombra inferior. Indica un rechazo de precios más bajos.
    ta.CDLINVERTEDHAMMER #Vela con un cuerpo pequeño en la parte inferior y una larga sombra superior. Indica un rechazo de precios más altos.
    
    ta.CDLDOJI #Vela donde el precio de apertura y cierre son casi iguales, mostrando indecisión.
    ta.CDLDRAGONFLYDOJI #Doji con una larga sombra inferior.
    ta.CDLGRAVESTONEDOJI #Doji con una larga sombra superior.
    ta.CDL3BLACKCROWS  #Tres largas velas negras consecutivas que cierran cerca de sus mínimos.
    ta.CDL3WHITESOLDIERS #Tres largas velas blancas consecutivas que cierran cerca de sus máximos.
    ta.CDLPIERCING #Tres largas velas blancas consecutivas que cierran cerca de sus máximos.
    ta.CDLDARKCLOUDCOVER #Similar al patrón de piercing, pero en reversa y durante una tendencia alcista.
    
    

    data=yf.download(ticker,period='1y',interval='1d')
    data_with_patterns = data.copy()
    pattern_list = ['ENGULFING', 'HAMMER', 'INVERTEDHAMMER', 'DOJI', 'DRAGONFLYDOJI', 'GRAVESTONEDOJI', '3BLACKCROWS', '3WHITESOLDIERS', 'PIERCING', 'DARKCLOUDCOVER']

    for pattern in pattern_list:
        data_with_patterns[f'CDL{pattern}'] = getattr(ta, f'CDL{pattern}')(data['Open'], data['High'], data['Low'], data['Close'])

    fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(20, 10))
    colors = mpf.make_marketcolors(up='#a83232', down='#32a88d')
    mpl_style = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=colors)
    mpf.plot(data, type='candle', ax=axs[0], style=mpl_style)
    for pattern in pattern_list:
        axs[1].plot(data_with_patterns[f'CDL{pattern}'], label=pattern)
    axs[1].set_title('Candlestick Patterns')
    axs[1].legend()
    plt.savefig(f'analytics\out\paterns\Candlestick_{ticker}.png')

    
def main():
    tickers=ticker_input()
    yf.pdr_override()
    data_ex = pdr.get_data_yahoo(tickers, start="2005-01-01", end="2024-04-10")
    level_of_volatility(data_ex)
    averge_return(data_ex)
    visualization_of_stock_data(data_ex)
    #tickers = ticker_QQQ()
    tickers_df, tickers_data = get_tickers_data(tickers)
    df_ticker_data = scatter_graph(tickers_data, tickers_df,tickers)
    averse,other = Risk_averse(df_ticker_data)
    taker = Risk_taker(df_ticker_data)
    for i in range(len(averse)):
        try:
            sr(averse[i],'averse')
            print(f'Support and Resistance for {averse[i]}')
            candlestick_chart(averse[i])
        except Exception as e:
            print(e)
    for i in range(len(taker)):
        try:
            sr(taker[i],'taker')
            print(f'Support and Resistance for {taker[i]}')
            candlestick_chart(taker[i])
        except Exception as e:
            print(e)
    for i in range(len(other)):
        try:
            sr(other[i],'other')
            print(f'Support and Resistance for {other[i]}')
            candlestick_chart(other[i])
        except Exception as e:
            print(e)
    
    
    

if __name__ == '__main__':
    main()