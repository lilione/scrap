from datetime import datetime
import gzip
import os
import ccs
import json
import logging
import time

logging_format = '%(asctime)-15s %(levelname)-8s %(name)-6s %(message)s'
logging.basicConfig(format=logging_format, level=logging.INFO)

sys = "bifinex"

def check_dir(directory):
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

def deal(coinPair):
    coinPair_dir = os.path.join(path, coinPair)
    check_dir(coinPair_dir)
    logging_dir = os.path.join(coinPair_dir, datetime.utcnow().strftime("%Y-%m-%d"))
    check_dir(logging_dir)
    try:
        response = ccs.bitfinex.public.orderbook(coinPair, group=0, limit_bids=1000, limit_asks=1000)
        logging.info("scraping... " + coinPair)
        gzip_file_path = os.path.join(logging_dir, datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S") + ".gz")
        with gzip.open(gzip_file_path, 'w') as f:
            f.write(str(response).encode("ascii"))
    except Exception as e:
        logging.info(e.args)
    time.sleep(2)

result_dir = '../results'
check_dir(result_dir)
path = os.path.join(result_dir, sys)
check_dir(path)

response = ccs.bitfinex.public.symbols()
coinPairs = json.loads(response)

while (True):
    for coinPair in coinPairs:
        deal(coinPair)