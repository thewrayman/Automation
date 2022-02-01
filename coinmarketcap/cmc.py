import sys
import json
import requests
import jmespath

f = open("api.json")
api_json = json.load(f)

BASE_URL = "https://pro-api.coinmarketcap.com"

headers = {
  "Accepts": "application/json",
  "X-CMC_PRO_API_KEY": api_json["cmc"],
}


def get_quote(ticker):
    api_path = "/v1/cryptocurrency/quotes/latest"
    params = {"symbol": ticker}

    r = requests.get(f"{BASE_URL}{api_path}", params=params, headers=headers)

    usd_price = jmespath.search(f"data.{ticker.upper()}.quote.USD.price", r.json())

    return usd_price


if __name__ == '__main__':
    target_coin = sys.argv[1]
    get_quote(target_coin)
