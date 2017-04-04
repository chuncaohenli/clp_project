import json
from Item import *

# read 10 comments
def getComments(jcontent,productID):
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

def readJD(filename,productID):
    # read json file
    fopen = open(filename,'r')
    content = fopen.readline()
    jcontent = json.loads(content)

    comment_list = getComments(jcontent,productID)
    hotCommentTag_list = getHotTag(jcontent)
    return [comment_list,hotCommentTag_list]
