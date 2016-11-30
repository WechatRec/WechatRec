#!/usr/bin/python
# @param1: input file path
# @param2: output file path

import sys
import re

if len(sys.argv) == 3:
    inp = open(sys.argv[1], 'r')
    out = open(sys.argv[2], 'w')

    content = inp.readlines()
    content = set(content)
    inp.close()

    filt = re.compile('^[-\w]*$')
    for wechatid in content:
        wechatid = wechatid.strip()
        if filt.match(wechatid):
            out.write('%s\n' % wechatid)

    out.close()
