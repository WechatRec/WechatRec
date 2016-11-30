# -*- coding: utf-8 -*-
#!/usr/bin/python
# @param1: wechatid file path
# @param2: starting offset in file (get articles for the following n wechatids)
# @param3: number of wechatids processed per batch

# imports
from wechatsogou.tools import *
from wechatsogou import *
from lxml import etree
import itertools
import logging
import logging.config
import sys
import time

# log
logging.config.fileConfig('/home/tatianajin/Wechat/logging.conf')
logger = logging.getLogger()

# instances
wechats = WechatSogouApi()

def get_articles(wid):
    try:
        data = wechats.get_gzh_message(wechatid=wid)
        sys.stderr.write('got data from wid %s' % wid)
    except:
        sys.stderr.write('cannot get data for wid %s\n' % wid)
        data = []
    for d in data:
        if d['type'] == '49':
            try:
                article = wechats.deal_article_content(url=d['content_url'])
                page = etree.HTML(article)
                pure_txt = ' '.join(list(filter(None, page.xpath('//body//*/text()'))))
                timestamp = d['datetime']
                with open('/home/tatianajin/Wechat/data/%s/%s_%s.txt' % (wid, wid, timestamp), 'w') as out_article:
                    out_article.write('%s\n' % pure_txt)
            except:
                sys.stderr.write('cannot get page content for %s: %s\n' % (wid, d['content_url']))

def get_articles_from_wechatid(id_file = '../data/id/id.txt', start_offset = 0, throughput = 5):
    f = open(id_file, 'r')
    with open(id_file, 'r') as f:
        for wid in itertools.islice(f, start_offset, start_offset + throughput): # read n=throughput wechatid each time
            get_articles(wid.strip())

if __name__ == '__main__':
    if len(sys.argv) == 4:
        get_articles_from_wechatid(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        get_articles_from_wechatid()
