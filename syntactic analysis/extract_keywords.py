# encoding=utf-8
import jieba
import jieba.posseg as pseg
import jieba.analyse
import traceback
import utils
comments = ""
path = './jd_review/review_3133817/3133817_'
for i in range(2):
    try :
        data = utils.readJD(path+str(i)+'.json','3133817')
        # comments.extend(data[0])
        for contents in data[0]:
            comments += "\n" +contents.content
        # num_hottag = len(data[1])
    except Exception:
        traceback.print_exc()
        continue
print(comments)
# jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
# sentence 为待提取的文本
# topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
# withWeight 为是否一并返回关键词权重值，默认值为 False
# allowPOS 仅包括指定词性的词，默认值为空，即不筛选
print('='*40)
print('3. Keyword extraction')
print('-'*40)
print(' TF-IDF')
print('-'*40)

output1 = open('TF_IDFextract.txt','w')
print('only n')
for x, w in jieba.analyse.extract_tags(comments,topK=50, withWeight=True,allowPOS=('n')):
    print('%s %s' % (x, w))

print('all')
output1.write('all'+'\n')
for x, w in jieba.analyse.extract_tags(comments,topK=50, withWeight=True):
    print('%s %s' % (x, w))
    # output1.write('%s %s' % (x, w))


print('-'*40)
print(' TextRank')
print('-'*40)
print('only n')
for x, w in jieba.analyse.textrank(comments,topK=50, withWeight=True,allowPOS=('n')):
    print('%s %s' % (x, w))
print('all')
for x, w in jieba.analyse.textrank(comments,topK=50, withWeight=True):
    print('%s %s' % (x, w))


