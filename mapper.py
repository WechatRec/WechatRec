#!/usr/bin/env python



#@param1: cache path for jieba

# @param2: number of tokens in a shingle



import jieba

import sys

import os

#from gensim import corpora, models, similarities



#jieba.load_userdict('dict.txt')

##extract all possible words

jieba.dt.tmp_dir = sys.argv[1]



def mode_precise(k,f):

    shin_list=[]

    #f= open('dat','r')

    for line in f:
        
        name,raw=line.strip().decode('UTF-8').split('\t')
        word_list = list(jieba.cut(raw, cut_all = False, HMM=False))
        stopw = set([line.strip().decode('UTF-8') for line in open('stopwords.txt').readlines()])

        ## delete the stopword and append k nearest one

        

        offset=0

        for i in range(len(word_list)):

            if word_list[i-offset] in stopw or word_list[i-offset]==' ':

                del word_list[i-offset]

                offset+=1



        for i in range(len(word_list)-k):

            string=""

            for j in range(k):

                string+=word_list[i+j]

            shin_list.append(string)

        #print(word_list)

        for j in shin_list:

            j=j.encode('UTF-8')
            name=name.encode('UTF-8')

            print('%s\t%s' % (j, name))



def mode_all(f):

    raw=f.read()

    raw=raw.replace('\n',' ')

    word_list = jieba.cut(raw, cut_all = True, HMM=False)

    stopw = [line.strip() for line in open('stopwords.txt').readlines()]



    word_list=set(word_list)-set(stopw)

    for i in word_list:

        i=i.encode('UTF-8')

        print('%s\t%s' % (i, os.environ['mapreduce_map_input_file'].split('/')[-1]))


f=sys.stdin
#f=open('test/1','rb')
mode_precise(int(sys.argv[2]),f)

#mode_all(f)
