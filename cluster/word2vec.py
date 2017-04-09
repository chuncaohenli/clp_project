#encoding=utf-8
# 引入 word2vec
from gensim.models import word2vec
# 引入日志配置
import logging
import jieba
import jieba.posseg as pseg
import utils
import traceback
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# read data
comments = []
num_hottag = 0
path = './jd_review/review_3133817/3133817_'
sentences = []
corpus = {}
word_vec = {}
# for i in range(4901):
#     try :
#         data = utils.readJD(path+str(i)+'.json','3133817')
#         comments.extend(data[0])
#         num_hottag = len(data[1])
#     except Exception:
#         traceback.print_exc()
#         continue
#

# for i,c in enumerate(comments):
#     seg_list = pseg.cut(c.content)
#     tmp = []
#     for word,flag in seg_list:
#         tmp.append(word)
#         if word not in corpus:
#             corpus[word] = [flag]
#         else:
#             corpus[word].append(flag)
#     sentences.append(tmp)



f_ltp = open('ltp_result.txt','r')
ll = f_ltp.readline().split('{')
sentences = eval(ll[0])
corpus = eval('{'+ll[1])
tmp = {}
for k in corpus.keys():
    nk = unicode(k,'utf-8')
    tmp[k] = corpus[k]

# 构建模型
model = word2vec.Word2Vec(sentences, min_count=1)
model.save('word2vec_model')

for k in corpus.keys():
    word_vec[k] = model.wv[k]

f = open('corpus.txt','w')
f.write(str(tmp)+'\n')
f.write(str(word_vec))
f.close()
