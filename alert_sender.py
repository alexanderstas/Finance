from secrets import robin_password, robin_username
import robin_stocks as rs
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secrets import gmail_pass, gmail_user


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
        # msg['Subject'] = subject
        body = message
        msg.attach(MIMEText(body, 'plain'))

        sms = msg.as_string()

        self.server.sendmail(gmail_user, self.sms_gateway[0], body)
        self.server.quit()


if __name__ == '__main__':
    alert = EmailSender()
    rs.login(username=robin_username, password=robin_password, expiresIn=86400, by_sms=True)

    symbols = [
        #{'ticker': 'POAI', 'min_target': 1.40, 'type': 'stock'},
        #{'ticker': 'SKLZ', 'min_target': 35.00, 'type': 'stock'},
        {'ticker': 'CCIV', 'min_target': 30.00, 'type': 'stock'},
        {'ticker': 'ZOM', 'max_target': 3.20, 'type': 'stock'}
    ]

    while True:
        for symbol in symbols:
            current_price = float(rs.get_stock_quote_by_symbol(symbol['ticker'])['ask_price'])
            if 'min_target' in symbol:
                if current_price <= symbol['min_target']:
                    alert.send_email(symbol["ticker"],
                                     f'[{symbol["ticker"]}] has dropped to {symbol["min_target"]}.\nwww.robinhood.com/stocks/{symbol["ticker"]} '
                                     )
                    symbol['min_target'] = 0
            else:
                if current_price >= symbol['max_target']:
                    alert.send_email(symbol["ticker"],
                                     f'[{symbol["ticker"]}] has risen to {symbol["max_target"]}.\nwww.robinhood.com/stocks/{symbol["ticker"]} '
                                     )
                    symbol['max_target'] = float("inf")
            time.sleep(5)
