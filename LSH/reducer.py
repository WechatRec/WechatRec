#!/usr/bin/env python
import sys


file=sys.stdin

dic=[]
a=[]
doc=[]
for i in file:
    d,t=i.split('\t')	#d word    t document_id
    t=t.strip()
    if t not in doc:
        doc.append(t)
    if d in dic:
        a[dic.index(d)].append(t)
    else:
        dic.append(d)
        a.append([t])

for i in range(len(dic)):
    wordInDoc = ''
    for doc_id in doc:
        freq = a[i].count(doc_id)
        if freq > 0:
            wordInDoc = '%s\t%s:%s' % (wordInDoc, doc_id, freq)
    print '%s%s' % (dic[i], wordInDoc)
