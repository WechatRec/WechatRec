# -*- coding: utf-8 -*-

# 导入包
from wechatsogou.tools import *
from wechatsogou import *
import logging
import logging.config
import json
import os
import random
import string
from time import sleep
import csv
from wechatsogou import config

# 日志
logging.config.fileConfig('logging.conf')
logger = logging.getLogger()

# 实例
ocr_config = {
     'type': 'ruokuai',
    'dama_name': config.dama_name,
    'dama_pswd': config.dama_pswd,
    'dama_soft_id': config.dama_soft_id ,
    'dama_soft_key': config.dama_soft_key
}
# wechats = WechatSogouApi(ocr_config=ocr_config)
wechats = WechatSogouApi()
path = 'output'
wcidFile = 'wcids' + '.txt'
cnt = 0
# 对于上面获取的文章链接，需要处理,注意此方法获取的`yuan`字段是文章固定地址，应该存储这个
with open(os.path.join(path, wcidFile), 'r') as infile:
    while (cnt < 293):  # start from this number of wechatid
        infile.readline()
        cnt += 1
    for line in infile:
        sleep(random.uniform(4, 9)) # change it if needed
        wechat_id = line.rstrip()
        print('wechatid: ', wechat_id)

        #  find wecahid's basic information
        info = wechats.get_gzh_info(wechatid = wechat_id)

        subPath = os.path.join(path, wechat_id)
        if not os.path.exists(subPath):
            os.makedirs(subPath)
        filename = 'info.txt'
        with open(os.path.join(subPath, filename), 'w') as outfile:
            json.dump(info, outfile)

        #  extract recent articles' content
        messages = wechats.get_gzh_message(wechatid = wechat_id)
        article_num = 1
        for m in messages:
            sleep(random.random()*4+2) # change it if needed
            if m['type'] == '49':
                article_info = wechats.deal_article(m['content_url'])
                subPath = os.path.join(path, wechat_id)
                if not os.path.exists(subPath):
                    os.makedirs(subPath)
                filename = str(article_num) + '.txt'
                with open(os.path.join(subPath, filename), 'w+') as outfile:
                    json.dump(article_info, outfile)
                article_num += 1
        print("finish No. {} id.".format(cnt))
        cnt += 1


