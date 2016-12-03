#!/usr/bin/env python
import sys

file=sys.stdin
a=[]
doc_id = None
for line in file:
    n,d=line.strip().split('\t') # doc_id, shingle_id
    if doc_id == n:
        a.append(d)
    else:
        if doc_id != None:
            print '%s\t%s' % (doc_id, '\t'.join(a))
        doc_id = n
        a = [d]
if doc_id != None:
    print '%s\t%s' % (doc_id, '\t'.join(a))
