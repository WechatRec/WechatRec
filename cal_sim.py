#!/usr/bin/python
# has TODO
# @param1: path to the file storing clusters
# @param2: path to the file storing doc vectors
# @param3: number of topics
# sample cmd: python cal_sim.py LSH/doc_cluster.txt LSH/out_lda/part-00000 2

import os, sys
from gensim import corpora, models, similarities

# global variables
cluster_path = sys.argv[1]
vector_path = sys.argv[2]
num_topics = int(sys.argv[3])
doc_dict = dict()

# get vector representation of docs
def get_vector(vector_path):
    with open(vector_path, 'r') as f:
        for line in f:
            line = line.strip().split()
            doc_dict[line[0]] = [(int(word.split(':')[0]), int(word.split(':')[1])) for word in line[1:]]

get_vector(vector_path)
# load clusters of documents
f1 = open(cluster_path, 'r')
for line in f1: # for each cluster, perform lda
    doc_ids = line.strip().split()
    # get vector representation of each doc in the cluster
    docs = [doc_dict.get(doc) for doc in doc_ids]
    # calculate tfidf
    tfidf = models.TfidfModel(docs)
    docs_tfidf = tfidf[docs]
    # fit lda model
    lda = models.LdaModel(docs_tfidf, num_topics = num_topics)
# index for similarity queries
    docs_lda = lda[docs_tfidf]
    index = similarities.MatrixSimilarity(docs_lda)
#TODO save index to file ?
    idx = 0
    for doc_lda in docs_lda:
        related = sorted(enumerate(index[doc_lda]), key=lambda item:item[-1], reverse=True)
        related = ['%s:%.3f' % (doc_ids[r[0]], r[1]) for r in related]
        print '%s\t%s' % (doc_ids[idx], '\t'.join(related))
        idx += 1
f1.close()
