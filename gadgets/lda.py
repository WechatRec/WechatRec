import jieba, os
from gensim import corpora, models, similarities


train_set = []


walk = os.walk('C:\\Users\\Sun Yutian\\Desktop\\test')
for root, dirs, files in walk:
        for name in files:
                f = open(os.path.join(root, name), 'r')
                raw = f.read()
                word_list = list(jieba.cut(raw, cut_all = False, HMM=True))
                train_set.append(word_list)


dic = corpora.Dictionary(train_set)
corpus = [dic.doc2bow(text) for text in train_set]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lda = models.LdaModel(corpus_tfidf, id2word = dic, num_topics = 10)
corpus_lda = lda[corpus_tfidf]

f= open('dat','r')
raw=f.read()
word_list = list(jieba.cut(raw, cut_all = False, HMM=True))
vec_bow=dic.doc2bow(word_list)
vec_lda=lda[vec_bow]

index = similarities.MatrixSimilarity(lda[corpus])
sims = index[vec_lda]
print(list(enumerate(sims))) 
