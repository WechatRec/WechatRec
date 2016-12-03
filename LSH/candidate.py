#!/usr/bin/env python

import sys

prev_doc = None
candidates = set()
for line in sys.stdin:
    doc, can = line.strip().split('\t')
    if doc == prev_doc:
        candidates.add(can)
    else:
        if prev_doc != None and len(candidates) > 0:
            print '%s\t%s' % (prev_doc, ','.join(candidates))
        candidates = set([can])
        prev_doc = doc
if prev_doc != None and len(candidates) > 0:
    print '%s\t%s' % (prev_doc, ','.join(candidates))
