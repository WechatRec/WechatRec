# -*- coding: utf-8 -*-
# @param1: id file path
import sys
from lxml import etree
from wechatsogou.tools import *
from wechatsogou import *
import get_article as ga
import logging
import logging.config
import os
import re

logging.config.fileConfig('/home/tatianajin/Wechat/logging.conf')
logger = logging.getLogger()
wechats = WechatSogouApi()
filt = re.compile('^[-\w]*$')

# TODO use bloom filter to detect if wechatid is already in list
id_file = open('/home/tatianajin/Wechat/data/id/id.txt', 'r')
wechatid_set = set(id_file.read().split('\n'))
id_file.close()

def get_id_from_url(urls = None): # read article url, print wechatid
    if urls == None: # no url is passed, read from stdin
        urls = sys.stdin
    out = None
    if len(sys.argv) == 2:
        out = open(sys.argv[1], 'a')
    else:
        sys.stderr.write('no output file specified, print to stdout\n')
    for line in urls:
        this_url = line.strip()
        text = wechats._get(this_url, 'get', host='mp.weixin.qq.com')
        try:
            page = etree.HTML(text)
            wechatid = page.xpath('//p[@class="profile_meta"]/span/text()')[0]
            if filt.match(wechatid) and wechatid not in wechatid_set:
                if out == None:
                    print wechatid
                else:
                    out.write('%s\n' % wechatid)
                    wechatid_set.add(wechatid)
                    if not os.path.exists('/home/tatianajin/Wechat/data/%s' % wechatid):
                        os.makedirs('/home/tatianajin/Wechat/data/%s' % wechatid)
                    #try:
                        #ga.get_articles(wechatid)
                    #except:
                    #    pass

        except:
            sys.stderr.write('html parse error: cannot get id from url %s' % this_url)
            continue
    if out != None:
        out.close()

def get_urls_from_text(text):
    page = etree.HTML(text)
    return page.xpath('//li/div[2]/h3/a/@href')

def get_id_from_recent():
    kinds = range(20)
    for kind in kinds:
        page_iter = 0
        sys.stderr.write("kind %d\n" % kind)
        url = 'http://weixin.sogou.com/pcindex/pc/pc_' + str(kind) + '/pc_0.html'
        try:
            text = wechats._get(url)
        except:
            text = None
            sys.stderr.write("invalid url: %s\n" % url)
        has_more = True
        miss_cnt = 0
        while has_more:
            page_iter += 1
            if text != None:
                urls = get_urls_from_text(text)
                get_id_from_url(urls)
            page_idx = str(page_iter)
            url = 'http://weixin.sogou.com/pcindex/pc/pc_' + str(kind) + '/'+page_idx+'.html'
            sys.stderr.write("get page %d\n" % page_iter)
            try:
                text = wechats._get(url)
            except:
                miss_cnt += 1
                sys.stderr.write("invalid page count: %d\n" % miss_cnt)
                text = None
                if miss_cnt == 2:
                    has_more = False

if __name__ == '__main__':
    get_id_from_recent()
