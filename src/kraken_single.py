import os

import ccs
import json

import time

path = '../records'

coinA = "ETH"
coinB = "USD"

sleepTime = 20

while (True):
    print(time.asctime( time.localtime(time.time()) ) + '\tscripting...')

    file = os.path.join(path, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ".txt")
    f = open(file, "w")

    response = ccs.kraken.public.getOrderBook(coinA + coinB)
    map = json.loads(response)
    result = map["result"]["X" + coinA + "Z" + coinB]

    asks = result["asks"]
    f.write('asks {}\n'.format(len(asks)))
    for ask in reversed(asks):
        f.write('{}\n'.format(str(ask)))

    bids = result["bids"]
    f.write('bids {}\n'.format(len(bids)))
    for bid in bids:
        f.write('{}\n'.format(str(bid)))

    f.close()

    time.sleep(sleepTime)