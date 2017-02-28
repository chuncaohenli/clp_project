import json
from Item import *

# read json file
fopen = open('jd_review/3133817_0.json','r')
content = fopen.readline()
jcontent = json.loads(content)

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


comment_list = getComments(jcontent)
hotCommentTag_list = getHotTag(jcontent)