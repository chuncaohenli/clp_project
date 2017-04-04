#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback
import utils

from Item import *
import sys, os
from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

ROOTDIR = 'F:\python proj\ltp-data-v3.3.1'
sys.path = [os.path.join(ROOTDIR, "lib")] + sys.path

# Set your own model path
MODELDIR=os.path.join(ROOTDIR, "ltp_data")



# read json file
# fopen = open('jd_review/3133817_4.json','r')
# content = fopen.readline()
# jcontent = json.loads(content)



# read 10 comments
def getComments(jcontent):
    res = []
    for cl in jcontent['comments']:
        tmp = Comment(cl['content'],cl['creationTime'],cl['id'],'3133817')
        res.append(tmp)
    return res
# read hot tags for this product
def getHotTag(jcontent):
    res = []
    for hl in jcontent['hotCommentTagStatistics']:
        tmp = HotTag(hl['name'],hl['productId'],hl['count'])
        res.append(tmp)
    return res

# sentence = SentenceSplitter.split(paragraph)[0]
# segmentor = Segmentor()
# segmentor.load(os.path.join(MODELDIR, "cws.model"))
# words = segmentor.segment(sentence)
# print "\t".join(words)
# postagger = Postagger() # 初始化实例
# postagger.load(os.path.join(MODELDIR, "pos.model"))
# postags = postagger.postag(words)  # 词性标注
# print '\t'.join(postags)
dict = {}

# comment_list = getComments(jcontent)

comments = []
path = './jd_review/review_3133817/3133817_'
for i in range(4901):
    try :
        data = utils.readJD(path+str(i)+'.json','3133817')
        comments.extend(data[0])
        num_hottag = len(data[1])
    except Exception:
        traceback.print_exc()
        continue

segmentor = Segmentor()
segmentor.load(os.path.join(MODELDIR, "cws.model"))
postagger = Postagger() # 初始化实例
postagger.load(os.path.join(MODELDIR, "pos.model"))
parser = Parser()
parser.load(os.path.join(MODELDIR, "parser.model"))
for each in comments:
    # paragraph = each.content.encode('raw_unicode_escape')
    paragraph =  each.content.encode('UTF-8')
    review_id = each.id
    sentences = SentenceSplitter.split(paragraph)
    for sentence in sentences:
        words = segmentor.segment(sentence)
        # print "\t".join(words)

        postags = postagger.postag(words)  # 词性标注
        # print '\t'.join(postags)
        for (index,tag) in enumerate(postags):
            if tag == 'a':
                if postags[index-2] == 'n' and postags[index-1] == 'n':
                    # n n a
                    adj = words[index]
                    nn = words[index-2] + words[index-1]
                    print nn + " "  + adj
                elif postags[index-1] == 'n':
                    # n n a
                    adj = words[index]
                    nn = words[index-1]
                    print nn + " "  + adj
                elif postags[index-2] == 'n' and postags[index-1] == 'd':
                    if postags[index-3] == 'j' or postags[index-3] == 'v' :
                        # n d a
                        adj = words[index]
                        nn = words[index-3] + words[index-2]
                        dd = words[index-1]
                        print nn + " " + dd + " " + adj
                        adj = dd + " " + adj
                    else:
                        # n d a
                        adj = words[index]
                        nn = words[index-2]
                        dd = words[index-1]
                        print nn + " " + dd + " " + adj
                        adj = dd + " " + adj
                elif postags[index-3] == 'n' and postags[index-2] == 'd' and postags[index-1] == 'v':
                    # n d v a
                    adj = words[index]
                    nn = words[index-3]
                    dd = words[index-2]
                    print nn + " " + dd + " " + adj
                    adj = dd + " " + adj
                elif postags[index-3] == 'n' and postags[index-2] == 'a' and postags[index-1] == 'd':
                    # n a d a
                    adj = words[index]
                    nn = words[index-3]
                    dd = words[index-1]
                    print nn + " " + dd + " " + adj
                    adj = dd + " " + adj
                else:
                    continue
                # 存的时候每个特征(np或vp)，存储d+adj（有些只含有adj），对应文档编号。
                if nn in dict:
                    if adj in dict[nn]:
                        dict[nn][adj].add(review_id)
                    else:
                        dict[nn][adj] = set()
                        dict[nn][adj].add(review_id)
                else:
                    dict[nn] = {}
                    if adj in dict[nn]:
                        dict[nn][adj].add(review_id)
                    else:
                        dict[nn][adj] = set()
                        dict[nn][adj].add(review_id)
        arcs = parser.parse(words, postags)
        # print "\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)
    # for word, flag in words:
    #     if flag == "n":
    #         if word in d:
    #             d[word] += 1
    #         else:
    #             d[word] = float(1)
    #     print('%s %s' % (word, flag))
    # print(repr(d).decode('unicode-escape'))
# hotCommentTag_list = getHotTag(jcontent)
# for i in dict:
#     print json.dumps(dict[i], encoding="UTF-8", ensure_ascii=False)
print dict