import asyncio
import requests
import threading
import logging
from datetime import datetime, timedelta

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', level=logging.INFO)


class BinanceAutoBuy():
    def market(self):

    def __init__(self, *args, **kwargs):

        self.logger = logging.getLogger(__name__)

        self.boxApiEndpoint = 'https://www.binance.com/bapi/nft/v1/private/nft/mystery-box/purchase'
        self.authCheckEndpoint = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-mystery/collection/page'
        self.nftApiEndpoint = 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/order-create'

        self.id = kwargs.get('id')
        self.amount = kwargs.get('amount')
        self.threadsNum = kwargs.get('threads')
        self.runAt = 0
        self.headers = kwargs.get('headers')
        self.cookies = {
            "cookies": self.headers['Cookie']
        }

    def authCheck(self):

        try:

            authTestData = {
                "openStatus": 0,
                "page": 1,
                "pageSize": 16
            }

            request = requests.post(
                self.authCheckEndpoint, headers=self.headers, cookies=self.cookies, json=authTestData)
            response = request.json()

            if request.status_code == 200:
                if response['code'] == '000000':
                    self.logger.info('Success login to account!')
                else:
                    self.logger.info("Error, check your credentials!")
            else:
                self.logger.error(
                    f'Bad status code. Try again. Response status code - {request.status_code}')

        except Exception as e:
            self.logger.error(f'Error {str(e)}')
            pass

    def buyPacksProccess(self):

        try:
            buyData = {
                'number': f"{self.amount}",
                'productId': f"{self.id}"
            }
            
            while True:
                timeInterval = (
                    datetime.utcnow() + timedelta(seconds=self.runAt)).isoformat(' ', 'seconds')
                timeInterval = timeInterval[11:]

                if timeInterval >= '09:59:58':
                    request = requests.post(
                        self.boxApiEndpoint, headers=self.headers, cookies=self.cookies, json=buyData)
                    response = request.json()

                    if request.status_code == 200:
                        if response['success'] == True:
                            self.logger.info(
                                f'Successfully bought - {self.amount} packs')
                            break
                        elif response['success'] == False:
                            self.logger.info(
                                f'Cannot buy - {self.amount} packs. Error - {response}')

                    else:
                        self.logger.error(
                            f'Bad status code. Try again. Response status code - {request.status_code}')
                else:
                    now = datetime.utcnow().isoformat(' ', 'seconds')[11:]
                    self.logger.info(
                        f'Too early. Current time - {now}. Timeinterval - {timeInterval}')

                asyncio.sleep(0.5)

        except Exception as e:
            self.logger.error(f'Error {str(e)}')
            pass


    def run(self):
        for i in range(self.threadsNum):
            thread = threading.Thread(
                target=self.buyPacksProccess, name=f'Thread - {i}')
            thread.start()
        

if __name__ == "__main__":

    print("Menu:\n1 - check auth\n2 - run bot\n3 - market\n")

    id = *
    threadNum = 25
    runAt = 0
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru,en;q=0.9",
        "bnc-uuid": "f*",
        "Cache-Control": "max-age=0",
        "clienttype": "web",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "content-type": "application/json",
        "Cookie":"p20t=web.*.*",
        "csrftoken": "*",
        "device-info": "*=",
        "fvideo-id": "*",
        "Host": "www.binance.com",
        "lang": "ru",
        "Origin": "https://www.binance.com",
        "Referer": "https://www.binance.com/ru/nft/balance?tab=boxes",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.1.932 Yowser/2.5 Safari/537.36",
        "x-trace-id": "*-0eb3-40d8-a082-*",
        "x-ui-request-trace": "*-0eb3-40d8-a082-*",
        "x-nft-checkbot-sitekey": "*",
        "x-nft-checkbot-token": "*"
    }
    bot = BinanceAutoBuy(id=id, amount=1, threads=threadNum, headers=headers)
    n = int(input("Enter function number: "))

    if n == 1:
        bot.authCheck()
    elif n == 2:
        bot.run()
    elif n == 3:
        bot.market()
