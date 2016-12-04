#!/usr/bin/python

import sys

f=sys.stdin
f2=open('inter','w')
count=0
g=""
for line in f:
    a=line.strip().split('\t')[1]
    g+=str(count)+'\t'+a+'\n'
    count+=1

f2.write(g)
