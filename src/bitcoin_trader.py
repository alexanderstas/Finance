import robin_stocks as rs
from secrets import robin_password, robin_username
import time
import numpy as np

bank = 1000.00
m_trend = 0
start_y = float(rs.crypto.get_crypto_quote('BTC')['ask_price'])
data = [start_y for x in range(15)]
x_axis = [x for x in range(15)]
slopes = [0 for x in range(3)]

previous_sell_price = float(rs.crypto.get_crypto_quote('BTC')['ask_price'])
previous_buy_price = float(rs.crypto.get_crypto_quote('BTC')['ask_price'])


def fake_buy(symbol, limit_price):
    current_price = float(rs.crypto.get_crypto_quote(symbol)['ask_price'])
    fractional_shares_to_buy = bank / current_price

def fake_sell():
    pass

def buy():
    price_per_share = float(rs.crypto.get_crypto_quote('BTC')['ask_price'])
    shares = .05 / price_per_share
    rs.orders.order_buy_crypto_limit('BTC', .00001, round(price_per_share, 2), timeInForce='gtc')

def get_trend_slope():
    x = np.array(x_axis)
    y = np.array(data)
    m, b = np.polyfit(x, y, 1)
    slopes.append(m)
    del slopes[0]
    return m


def update_data(val):
    data.append(val)
    del data[0]


def get_current_price(symbol):
    return float(rs.crypto.get_crypto_quote('BTC')['ask_price'])


def slope_becoming_larger():
    '''
    Check if slope is negative and has been becoming larger for last three price queries.
    '''
    if slopes[0] < slopes[1] < slopes[2]:
        return True
    else:
        return False


def slopes_negative_enough():
    pass


if __name__ == '__main__':

    rs.login(username=robin_username, password=robin_password, expiresIn=86400, by_sms=True)

    invested = False

    while True:
        # TODO: Create simple algorithm to determine of BTC is trending up or down over the last 1 minute
        #   and use this to influence (2).
        while not invested:
            '''
            (1) Get current price of crypto and update data.
            (2) If current price is X% lower than previous sell price and slope of trend line is < 0 and
                has gotten larger for three consecutive times, place limit order for available 
                balance and wait 30 seconds.
            (3a) If limit order was executed, begin while loop for invested == True.
            (3b) If limit order was not executed, repeat invested == False.
            '''
            # (1)
            current_price = get_current_price('BTC')
            update_data(current_price)

            # (2)
            m_trend = get_trend_slope()
            if slope_becoming_larger() and slopes_negative_enough():


        while invested:
            '''
            (1) Get current price of crypto.
            (2) If current price is more than Y% higher than previous purchase price, place limit order
            to sell full balance and wait 30 seconds.
            (3a) If limit order was executed, begin loop for invested == False.
            (3b) If limit order was not executed, repeat invested == True.
            '''
            current_price = float(rs.crypto.get_crypto_quote('BTC')['ask_price'])


    rs.logout()
