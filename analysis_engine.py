import pandas as pd
import numpy as np
import math
import talib as ta
from alert_sender import EmailSender
import robin_stocks as rs
from secrets import robin_password, robin_username
import json
import time


class Engine(EmailSender):

    def __init__(self, path_to_csv, balance):
        EmailSender.__init__(self)
        self.path_to_csv = path_to_csv
        self.df = self.load_csv()
        self.add_MACD_cols()
        self.balance = balance
        self.shares = 0
        self.risk = .02
        self.buy('2010-01-05')
        print(self.df)

    def load_csv(self):
        return pd.read_csv(self.path_to_csv)

    def add_MACD_cols(self):
        self.df['macd'], self.df['macdsig'], self.df['macdhist'] = ta.MACD(np.asarray(self.df['Close']),
                                                                           fastperiod=12, slowperiod=26, signalperiod=9)
        self.df.set_index('Date', inplace=True)

    def buy(self, date):
        new_shares = math.floor(self.risk * self.balance / self.df.loc[date]['Open'])
        self.balance -= self.df.loc[date]['Open'] * new_shares
        self.shares += new_shares


def get_news_formatted(ticker):
    articles = rs.get_news(ticker)
    news = []
    for article in articles:
        news.append(f'{ticker} -- {article["published_at"]} -- {article["title"]} \n {article["url"]}')
    return news


if __name__ == '__main__':

    es = EmailSender()

    rs.login(username=robin_username, password=robin_password, expiresIn=86400, by_sms=True)
    tickers = list(rs.build_holdings().keys())

    print(rs.crypto.get_crypto_quote('BTC'))

    # for article in get_news_formatted('TSLA'):
    #     es.send_email('AAPL', article)

    # for ticker in tickers:
    #     print(ticker, rs.stocks.get_fundamentals(ticker)[0]['market_cap'])

    # for ticker in tickers:
    #     for article in get_news_formatted(ticker):
    #         print(article)

    rs.logout()
