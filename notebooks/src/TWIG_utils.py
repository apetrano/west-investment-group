import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from polygon import RESTClient
import ray
from ray.util.multiprocessing import Pool
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def getTickerDailyDataSLOW(client, ticker="IBM", start="2023-01-01", end="2023-02-01"):
    print(f'Starting data pull for {ticker}...')
    data = []
    date_range = pd.date_range(start, end, freq='B')

    for business_day in date_range:
        try:
            response = client.stocks_equities_daily_open_close(symbol=ticker, date=str(business_day)[0:10])
            data.append([pd.to_datetime(response.from_) ,response.open, response.close, response.high, response.low, ticker])
        except:
            continue
    print(f'Ended data pull for {ticker}...')
    print(data)
    return pd.DataFrame(data, columns=['date', 'open', 'close', 'high', 'low', 'ticker'])

def get_ticker_data(args):
    client, ticker, date = args
    try:
        response = client.stocks_equities_daily_open_close(symbol=ticker, date=str(date)[0:10])
        return [pd.to_datetime(response.from_), response.open, response.close, response.high, response.low, ticker]
    except:
        return None

def get_ticker_daily_data(client, ticker="IBM", start="2023-01-01", end="2023-02-01"):
    print(f'Starting data pull for {ticker}...')
    data = []
    date_range = pd.date_range(start, end, freq='B')
    input_data = [(client, ticker, x) for x in date_range]

 
    # Use map() to parallelize the function calls
    with Pool() as pool:
         results = pool.map(get_ticker_data, input_data) 
  
    # Collect the results and remove any None values
    data = [result for result in results if result is not None]

    print(f'Ended data pull for {ticker}...')
  
    return pd.DataFrame(data, columns=['date', 'open', 'close', 'high', 'low', 'ticker'])

# Function that takes in two values from the ticker data and plots them
def createPlot(xvalue, yvalue, xlabel, ylabel, title, xvalue2=np.empty(0), yvalue2=np.empty(0)):
    fig, ax = plt.subplots()
    ax.plot(xvalue, yvalue)
    if xvalue2.size > 0:
        ax.plot(xvalue2, yvalue2)

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
   
        
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    ax.grid()
    fig.tight_layout()
    plt.show()