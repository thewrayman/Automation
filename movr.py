import sys
import time
from coinmarketcap.cmc import get_quote
from subscan.subscan import SubScan


def check_status(address):
    """
    Checks the MOVR staking details of the provided address and returns back information on the total gained
    and if there has been a new reward since the last check
    :param address: ETH address
    :return: JSON blob as to whether this check contained a new reward or not, and the reward amount, value in USD,
    """
    print("Checking status")

    movr = SubScan("moonriver")
    current_total, last_reward = movr.pull_raw_staking_history(address)
    total_movr = current_total

    movr_price = get_quote("movr")
    reward_usd = int(movr_price) * float(last_reward)
    total_usd = int(movr_price) * float(current_total)

    reward_movr = last_reward

    print(f"New staking reward of {last_reward} (${reward_usd})!\n"
          f"Your total is now {current_total} MOVR (${total_usd})!")

    response_json = {
        "movr_reward": float(reward_movr),
        "usd_reward": float(reward_usd),
        "movr_total": float(total_movr),
        "usd_total": float(total_usd),
        "movr_price": float(movr_price)
    }

    return response_json


if __name__ == '__main__':
    target_address = sys.argv[1]

    while 1:
        json = check_status(target_address)
        print(json)
        time.sleep(300)
