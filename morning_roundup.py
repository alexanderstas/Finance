from email_sender import EmailSender
from analysis_engine import get_news_formatted
import robin_stocks as rs
from secrets import robin_password, robin_username
from newscatcher import Newscatcher


if __name__ == '__main__':

    es = EmailSender()
    rs.login(username=robin_username, password=robin_password, expiresIn=86400, by_sms=True)

    tickers = list(rs.build_holdings().keys())


    # message = ''
    #
    # for ticker in tickers:
    #     for article in get_news_formatted(ticker):
    #         message += article+'\n'
    #
    # es.send_email(f'Morning Roundup', message)

    rs.logout()