import requests
from bs4 import BeautifulSoup
import time


class CryptPrice:
    # FOR PARSER
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.82 Mobile Safari/537.36",
        "accept": "*/*"}
    URL = 'https://coinmarketcap.com/currencies/ethereum'

    # API
    API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    def get_ETH_price_through_parser(self):
        try:
            r = requests.get(self.URL, headers=self.HEADERS)
            soup = BeautifulSoup(r.text, 'html.parser')

            price_div = soup.find(class_='priceValue')
            price_span = price_div.find('span')
            price_str = price_span.text.strip('$')
            price = float(price_str.replace(',', ''))

            return price

        except Exception as e:
            print(e.args)
            return

    def get_ETH_price_through_api(self):
        try:
            r = requests.get(self.API_URL, headers=self.HEADERS)
            price = r.json()['ethereum']['usd']
            return price

        except Exception as e:
            print(e.args)
            return

    @staticmethod
    def calculate_percentage_between_prices(previous_price, current_price):
        return current_price * 100 / previous_price - 100

    @staticmethod
    def notify_about_price_changes(percentage):
        if percentage > 1:
            return 1
        return 0


def get_time():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())


def main():

    ETH = CryptPrice()

    beginning_price = ETH.get_ETH_price_through_parser()
    beginning_time = get_time()

    previous_price = ETH.get_ETH_price_through_parser()
    current_price = 0.0
    list_of_price_changes = []

    start_time = time.time()
    one_hour = 3600

    while time.time() - start_time < one_hour:
        time.sleep(3)
        current_price = ETH.get_ETH_price_through_parser()
        percentage = abs(ETH.calculate_percentage_between_prices(previous_price, current_price))

        if ETH.notify_about_price_changes(percentage):
            price_change_data = {
                'previous_price': previous_price,
                'current_price': current_price,
                'percentage': percentage,
                'date': get_time()
            }
            list_of_price_changes.append(price_change_data)

            print("----------------- THE PRICE HAS CHANGED -----------------")
            print(f"The price has changed from {previous_price} to {current_price}\n"
                  f"The percentage difference is {percentage}")
            print("----------------- THE PRICE HAS CHANGED -----------------\n\n")

        previous_price = current_price

    print("----------------- THE REPORT -----------------")
    print(f"The beginning price was: {beginning_price}USD at {beginning_time}\n"
          f"The current price is {current_price}USD\n"
          f"The percentage difference is {abs(ETH.calculate_percentage_between_prices(beginning_price, current_price))}\n"
          "The list of price changes during 1 hour:")
    print(list_of_price_changes)
    print("----------------- THE REPORT -----------------")


if __name__ == "__main__":
    while True:
        main()
