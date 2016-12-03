#!/usr/bin/env python
import sys


file=sys.stdin
a=[]
b=[0,0,0]
for line in file:
    n,d=line.strip().split('\t')
    b[int(n)-1]+=1
    a.append(d)
print a,b


