import sys
import time
import schedule

from coinmarketcap.cmc import get_quote
from subscan.subscan import pull_raw_staking_history

startup = True
last_total = None


def check_status(address):
    """
    Checks the MOVR staking details of the provided address and returns back information on the total gained
    and if there has been a new reward since the last check
    :param address: MOVR address (ETH address)
    :return: JSON blob as to whether this check contained a new reward or not, and the reward amount, value in USD,
    """
    print("Checking status")
    global startup
    global last_total

    updated = False
    total_usd = 0
    reward_movr = 0
    reward_usd = 0

    current_total, last_reward = pull_raw_staking_history(address)
    total_movr = current_total

    if startup:
        movr_price = get_quote("movr")
        last_total = current_total

        startup = False
        total_usd = int(movr_price) * float(current_total)

        print("Started up")

    else:
        if current_total != last_total:
            last_total = current_total

            movr_price = get_quote("movr")
            reward_usd = int(movr_price) * float(last_reward)
            total_usd = int(movr_price) * float(current_total)

            updated = True
            reward_movr = last_reward

            print(f"New staking reward of {last_reward} (${reward_usd})!\n"
                  f"Your total is now {current_total} MOVR (${total_usd})!")

        else:
            print("nothing new")

    response_json = {
        "updated": updated,
        "movr_reward": float(reward_movr),
        "usd_reward": float(reward_usd),
        "movr_total": float(total_movr),
        "usd_total": float(total_usd)
    }

    return response_json


def test(address):
    check_status(address)
    global last_total
    last_total = 123
    check_status(address)


if __name__ == '__main__':
    target_address = sys.argv[1]

    while 1:
        json = check_status(target_address)
        print(json)
        time.sleep(300)