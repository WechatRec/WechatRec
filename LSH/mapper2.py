#!/usr/bin/env python
import sys
#from gensim import corpora, models, similarities

#jieba.load_userdict('dict.txt')
##extract all possible words

#f=open('inter','r')
f=sys.stdin
for line in f:
	a = line.strip().split('\t')[0]
	doc = line.strip().split('\t')[1:]
	for i in doc:
		print '%s\t%s' % (i, a)
