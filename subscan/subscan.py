import datetime
import sys
import json
import jmespath
import requests

f = open("api.json")
api_json = json.load(f)

BASE_URL = "https://{}.api.subscan.io"
MAX_PLACES = 18

headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_json["subscan"]
}


class SubScan:
    def __init__(self, chain):
        self.chain = chain
        self.base_url = BASE_URL.format(chain)

    def convert_number_to_decimal(self, value):
        total_decimal_points = len(str(value))
        prepend_str = "0." + ("0" * (MAX_PLACES-int(total_decimal_points)))

        total_value = prepend_str+str(value)

        return total_value

    def pull_raw_staking_history(self, address):
        api_path = "/api/scan/account/reward_slash"

        data = {
            "row": 100,
            "page": 0,
            "address": address
        }

        data = json.dumps(data)
        r = requests.post(f"{self.base_url}{api_path}", data=data, headers=headers)

        result_json = r.json()

        all_amounts = jmespath.search("data.list[].amount", result_json)
        latest_amount = jmespath.search("data.list[0].amount", result_json)

        total_sum = sum([int(i) for i in all_amounts])
        total_value = self.convert_number_to_decimal(total_sum)
        latest_reward = self.convert_number_to_decimal(latest_amount)

        return total_value, latest_reward


if __name__ == '__main__':
    target_address = sys.argv[1]

    movr = SubScan("moonriver")
    total, latest = movr.pull_raw_staking_history(target_address)
    print(total)
    print(latest)

