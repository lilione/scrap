import datetime
import gzip
import os
import ccs
import json
import logging
from multiprocessing import Process

logging_format = '%(asctime)-15s %(levelname)-8s %(name)-6s %(message)s'
logging.basicConfig(format=logging_format, level=logging.INFO)

sys = "kraken"

def check_dir(directory):
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

def deal(coinPair):
    coinPair_dir = os.path.join(path, coinPair)

    last = None

    while (True):
        try:
            response = ccs.kraken.public.getOrderBook(coinPair)

            if (response != last):
                logging.info("scripting... " + coinPair)
                file = os.path.join(coinPair_dir, datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S") + ".gz")
                f = gzip.open(file, "w")
                f.write(str(response).encode("ascii"))
                f.close()
                last = response
        except Exception as e:
            logging.info(e)

result_dir = '../results'
check_dir(result_dir)
path = os.path.join(result_dir, sys)
check_dir(path)

response = ccs.kraken.public.getTradableAssetPairs()
map = json.loads(response)
coinPairs = map["result"]

for key in coinPairs:
    print(coinPairs[key]['altname'])
    coinPair_dir = os.path.join(path, coinPairs[key]['altname'])
    check_dir(coinPair_dir)

    file = os.path.join(coinPair_dir, coinPairs[key]['altname'] + ".txt")

    f = open(file, "w")
    f.write(str(coinPairs[key]))
    f.close()

p = []
for key in coinPairs:
    p.append(Process(target=deal,args=(coinPairs[key]['altname'], )))
for proc in p:
    proc.start()
for proc in p:
    proc.join()

