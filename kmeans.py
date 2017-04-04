# encoding=utf-8
import jieba
import utils

# read data
comments = []
num_hottag = 0
path = 'jd_review/review_3133817/3133817_'
for i in range(6):
    data = utils.readJD(path+str(i)+'.json','3133817')
    comments.extend(data[0])
    num_hottag = len(data[1])

# tfidf

words_freq = {}
words_corpus = set()
cnt = 1
dic_comment = []
for i,c in enumerate(comments):
    seg_list = jieba.cut(c.content)

