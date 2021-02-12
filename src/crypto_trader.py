from secrets import robin_password, robin_username
import robin_stocks as rs
import time
from alert_sender import EmailSender


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def buy(name, quantity):
    ...


def attempt_sell(crypto, quantity):
    if crypto['current_price'] < (1 - theta) * crypto['current_max']:
        print(f'Sold {crypto["name"]}. Current: {crypto["current_price"]}, Max: {crypto["current_max"]}')


def update_max_min(cryptos):
    print_str = ''
    for crypto in cryptos:
        crypto['current_price'] = round(float(rs.get_crypto_quote(crypto['name'])['ask_price']), 2)
        # Update max
        if crypto['current_max'] < crypto['current_price']:
            crypto['current_max'] = round(crypto['current_price'], 2)
        # Update min
        if crypto['current_min'] > crypto['current_price']:
            crypto['current_min'] = round(crypto['current_price'], 2)
        print_str += f"[{bcolors.WARNING}{crypto['name']}{bcolors.ENDC}: Current: {bcolors.OKGREEN}{crypto['current_price']}{bcolors.ENDC}, Max: {bcolors.OKBLUE}{crypto['current_max']}{bcolors.ENDC}, Min: {bcolors.FAIL}{crypto['current_min']}{bcolors.ENDC}]"
    print(print_str)


if __name__ == '__main__':
    rs.login(username=robin_username, password=robin_password, expiresIn=86400, by_sms=True)

    theta = 0.001

    cryptos = [
        {'name': 'BTC', 'current_max': 0.0, 'current_min': float("inf"), 'current_price': 0.0},
        {'name': 'DOGE', 'current_max': 0.0, 'current_min': float("inf"), 'current_price': 0.0},
        {'name': 'ETH', 'current_max': 0.0, 'current_min': float("inf"), 'current_price': 0.0}
    ]

    # Main loop
    while True:
        update_max_min(cryptos)
        # for crypto in cryptos:
        #     attempt_sell(crypto, 100)
        time.sleep(1)
