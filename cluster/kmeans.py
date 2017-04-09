#encoding=utf-8
# 引入 word2vec

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from gensim.models import word2vec
from sklearn.cluster import KMeans
import numpy as np

model = word2vec.Word2Vec.load('word2vec_model')
#a =  model.most_similar([u'电池'])
# for b in a:
#     print b[0].encode('utf-8')
f = open('corpus.txt','r')
corpus = eval(f.readline().strip())
word_vec = {}

for k in corpus.keys():
    word_vec[k] = model.wv[k]


noun_corpus = set() # n nr ns nt nz
noun_arr = []
adj_corpus = set() # a ad an
adj_arr = []
adverb_corpus = set() # d
adverb_arr = []

for k,v in corpus.iteritems():
    if 'n' in v or 'nr' in v or 'nt' in v or 'nz' in v:
        noun_corpus.add(k)
    if 'a' in v or 'ad' in v or 'an' in v:
        adj_corpus.add(k)
    if 'd' in v:
        adverb_corpus.add(k)

for ele in noun_corpus:
    noun_arr.append(word_vec[ele])
for ele in adj_corpus:
    adj_arr.append(word_vec[ele])
for ele in adverb_corpus:
    adverb_arr.append(word_vec[ele])

kmeans_noun = KMeans(n_clusters=20, random_state=0).fit(np.asarray(noun_arr))

fcluster = open('noun_cluster.txt','w')
i = 0
for ele in noun_corpus:
    #fcluster.write(ele.encode('utf-8')+'\t'+str(kmeans_noun.labels_[i])+'\n')
    fcluster.write(ele+'\t'+str(kmeans_noun.labels_[i])+'\n')
    i+=1
fcluster.close()

kmeans_adj = KMeans(n_clusters=10, random_state=0).fit(np.asarray(adj_arr))
fcluster = open('adj_cluster.txt','w')
i = 0
for ele in adj_corpus:
    #fcluster.write(ele.encode('utf-8')+'\t'+str(kmeans_adj.labels_[i])+'\n')
    fcluster.write(ele+'\t'+str(kmeans_adj.labels_[i])+'\n')
    i+=1
fcluster.close()

kmeans_adverb = KMeans(n_clusters=10, random_state=0).fit(np.asarray(adverb_arr))
i = 0
fcluster = open('adverb_cluster.txt','w')
for ele in adverb_corpus:
    #fcluster.write(ele.encode('utf-8')+'\t'+str(kmeans_adverb.labels_[i])+'\n')
    fcluster.write(ele+'\t'+str(kmeans_adverb.labels_[i])+'\n')
    i+=1
fcluster.close()

print 1