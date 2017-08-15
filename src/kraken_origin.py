import datetime
import os
import ccs
import json

sleepTime = 20 #in seconds

def check_dir(directory):
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)


path = '../records'
check_dir(path)

response = ccs.kraken.public.getTradableAssetPairs()
map = json.loads(response)
coinPairs = map["result"]
for key in coinPairs:
    coinPair_dir = os.path.join(path, coinPairs[key]['altname'] + '/')
    check_dir(coinPair_dir)

    file = os.path.join(coinPair_dir, coinPairs[key]['altname'] + ".txt")

    f = open(file, "w")
    f.write(str(coinPairs[key]))
    f.close()

while (True):
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S") + '\tscripting...')

    for key in coinPairs:
        print(coinPairs[key]['altname'])

        coinPair_dir = os.path.join(path, coinPairs[key]['altname'] + '/')
        file = os.path.join(coinPair_dir, datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S") + ".txt")

        f = open(file, "w")

        response = ccs.kraken.public.getOrderBook(coinPairs[key]['altname'])
        f.write(response)

        f.close()

    datetime.time.sleep(sleepTime)

