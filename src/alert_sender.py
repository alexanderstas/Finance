from secrets import robin_password, robin_username
import robin_stocks as rs
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secrets import gmail_pass, gmail_user
import json
import pprint

PATH_TO_RETURN_TARGETS = '/Users/alexanderstas/Desktop/Finance/src/data/return_targets.txt'
PATH_TO_HOLDINGS = '/Users/alexanderstas/Desktop/Finance/src/data/holdings.txt'


class EmailSender:

    def __init__(self):
        self.sms_gateway = ['8457056286@vtext.com', 'stasalexanderj@gmail.com']
        self.smtp = "smtp.gmail.com"
        self.port = 587
        self.server = smtplib.SMTP(self.smtp, self.port)

    def send_email(self, subject, message):
        self.__init__()
        self.server.starttls()
        self.server.login(gmail_user, gmail_pass)

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = self.sms_gateway[0]
        msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))

        sms = msg.as_string()

        self.server.sendmail(gmail_user, self.sms_gateway[0], sms)
        self.server.quit()


def write_return_percentages():
    with open(PATH_TO_RETURN_TARGETS, 'w') as f:
        data = rs.build_holdings()
        final = {}
        for stock, stock_data in data.items():
            final[stock] = float(stock_data['percent_change'])
        f.write(json.dumps(final))


def get_return_percentages():
    with open(PATH_TO_RETURN_TARGETS) as f:
        data = f.read()
        return json.loads(data)


def write_holdings():
    with open(PATH_TO_HOLDINGS, 'w') as f:
        data = rs.build_holdings()
        f.write(json.dumps(data))


def get_holdings():
    with open(PATH_TO_HOLDINGS) as f:
        data = f.read()
        return json.loads(data)


def update_milestones(stock):
    milestones[stock] += 5


if __name__ == '__main__':
    alert = EmailSender()
    rs.login(username=robin_username, password=robin_password, expiresIn=86400, by_sms=True)

    # rs.export_completed_stock_orders('/Users/alexanderstas/Desktop/Finance/src/data/'))

    write_return_percentages()
    return_percentages = get_return_percentages()

    # Obtain current percentage_increase. Set next milestone to 5% higher.
    milestones = {}
    for key, value in return_percentages.items():
        milestones[key] = return_percentages[key] + 5

    while True:
        portfolio = rs.build_holdings()
        for ticker, position in portfolio.items():
            current_percent_increase = float(position['percent_change'])
            if current_percent_increase >= milestones[ticker]:
                update_milestones(ticker)
                print(f'Alert sent for {ticker}')
                alert.send_email(ticker, f' has increased by another {str(5)+"%"} for a {str(current_percent_increase)+"%"} increase. www.robinhood.com/stocks/{ticker}')
                time.sleep(1)
        time.sleep(1)


    # symbols = [
    #     {'ticker': 'POAI', 'min_target': 1.90, 'type': 'stock'},
    #     {'ticker': 'SKLZ', 'min_target': 35.00, 'type': 'stock'},
    #     {'ticker': 'CCIV', 'min_target': 30.00, 'type': 'stock'},
    #     {'ticker': 'ZOM', 'max_target': 3.20, 'type': 'stock'}
    # ]
    # while True:
    # for symbol in symbols:
    #     current_price = float(rs.get_stock_quote_by_symbol(symbol['ticker'])['ask_price'])
    #     if 'min_target' in symbol:
    #         if current_price <= symbol['min_target']:
    #             alert.send_email(symbol["ticker"],
    #                              f'[{symbol["ticker"]}] has dropped to {symbol["min_target"]}.\nwww.robinhood.com/stocks/{symbol["ticker"]} '
    #                              )
    #             symbol['min_target'] = 0
    #     else:
    #         if current_price >= symbol['max_target']:
    #             alert.send_email(symbol["ticker"],
    #                              f'[{symbol["ticker"]}] has risen to {symbol["max_target"]}.\nwww.robinhood.com/stocks/{symbol["ticker"]} '
    #                              )
    #             symbol['max_target'] = float("inf")
