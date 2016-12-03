#!/usr/bin/env python
import sys


file=sys.stdin

dic=[]
a=[]
for i in file:
    d,t=i.split('\t')
    t=t.strip()
    if d in dic:
	if t in a[dic.index(d)]:
		continue
	else:
        	a[dic.index(d)].append(t)
    else:
        dic.append(d)
        l=[t]
        a.append(l)


for i in range(len(dic)):
    print '%s\t%s' % (dic[i], '\t'.join(a[i]))



