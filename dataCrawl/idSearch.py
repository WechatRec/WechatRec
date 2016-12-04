from wechatsogou.tools import *
from wechatsogou import *
import logging
import logging.config
import json
import os
import random
import string
from time import sleep
import threading, multiprocessing

# 日志
logging.config.fileConfig('logging.conf')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# 实例
wechats = WechatSogouApi()

# corresponding directory and file
path = 'output'
wcidFile = 'raw_wcids' + '.txt'
if not os.path.exists(path):
    os.makedirs(path)


# 生成随机wechat_id，用于查询
def gen_id():
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    symbol = '_-'
    s = alpha + alpha.upper() + string.digits + symbol
    idLen = 3
    randomIds = []
    while idLen < 4:
        for i in range(pow(idLen, 8)):  # scales search times
            randomID = ''.join(random.sample(s, idLen))
            if randomID not in randomIds:
                randomIds.append(randomID)
        idLen += 1
    return randomIds
    logger.info('finish generation')
    print("finish generation")


# 基于生成的随机id进行搜索，保存得到的真实wechat_id
def search_store_real_id(q):
    random_ids = gen_id()
    for random_id in random_ids:
        logger.debug('wechatid: ', random_id)
        info = wechats.search_gzh_info(random_id, page=1)

        for i in range(len(info)):
            try:
                w = info[i]['wechatid']
                q.put(w)

            except KeyError:
                print("key error")


def listener(q):
    with open(os.path.join(path, wcidFile), 'a+') as outfile:
        print("file opened")
        while 1:
            wcid = q.get()
            if wcid == 'kill':
                break
            if wcid not in outfile.read():
                outfile.write(wcid + '\n')
                outfile.flush()


def main():
    manager = multiprocessing.Manager()
    q = manager.Queue()
    pool = multiprocessing.Pool()

    #  start listener
    watcher = pool.apply_async(listener, (q,))

    #  start workers
    jobs = []
    for i in range(50):
        job = pool.apply_async(search_store_real_id, args=(q,))
        jobs.append(job)

    for job in jobs:
        job.get()

    print("waiting for all subprocess done...")
    q.put("kill")
    pool.close()
    pool.join()
    print("all subprocess done.")
    # search_store_real_id(outfile)


if __name__ == "__main__":
    main()
