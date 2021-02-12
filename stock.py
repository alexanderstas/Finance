import requests
from secrets import finnhub_token
import time
import pandas as pd


class Stock:

    def __init__(self, ticker):
        self.column_names = {'c': "Current", 'h': "High", 'l': "Low", 'o': "Open", 'pc': "Previous Close", 't': "Date"}
        self.ticker = ticker
        self.df = pd.DataFrame(columns=self.column_names.values())

    def update(self):
        """
        Retrieves stock information from XXXXXX and appends it to the dataframe
        """
        r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={self.ticker}&token={finnhub_token}').json()

        # Convert time to date-time format
        r['t'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(r['t']))

        # Change headings to appropriate names and append
        self.df = self.df.append(
            dict((self.column_names[key], value) for (key, value) in r.items())
            , ignore_index=True)

if __name__ == "__main__":
    tickers = ['ARKG', 'ZOM', 'BNGO']

    stocks = []

    # Create Stocks
    for ticker in tickers:
        stocks.append(Stock(ticker))

    while True:
        for stock in stocks:
            stock.update()
        time.sleep(15)
