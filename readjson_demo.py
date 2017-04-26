import json
from Item import *

# read json file
fopen = open(r'D:\jd_data_0416\data\review_3133817\3133817_0.json','r')
content = fopen.readline()
jcontent = json.loads(content)
productID = '3133817'

# read 10 comments
def getComments(jcontent):
    res = []
    for cl in jcontent['comments']:
        tmp = Comment(cl['content'],cl['creationTime'],cl['id'],productID)
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
