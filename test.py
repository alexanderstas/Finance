import robin_stocks as rs
from secrets import robin_password, robin_username
import time
import matplotlib.pyplot as plt
import numpy as np

def view_crypto(period_of_visualization, symbol):

    x_axis = np.array([x for x in range(period_of_visualization)])
    start_y = float(rs.crypto.get_crypto_quote(symbol)['ask_price'])
    y_axis = np.array([start_y for x in range(period_of_visualization)])

    while True:
        y = float(rs.crypto.get_crypto_quote(symbol)['ask_price'])
        y_axis = np.append(y_axis, y)
        y_axis = np.delete(y_axis, 0)
        plt.clf()

        m, b = np.polyfit(x_axis, y_axis, 1)
        plt.plot(x_axis, m * x_axis + b)

        percent_change = str((y - start_y)/start_y*100)+'%'
        plt.suptitle(percent_change)
        plt.plot(x_axis, y_axis)
        plt.pause(0.5)

    plt.show()

if __name__ == '__main__':
    rs.login(username=robin_username, password=robin_password, expiresIn=86400, by_sms=True)

    view_crypto(300, 'BTC')

    rs.logout()
