# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import logging
import time
import json
import lxml.html
import traceback
import urllib
import re
import os
from constant import my_headers, my_proxies

date = time.strftime("%Y-%m-%d", time.localtime())

import random


def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return header


def setup_logging(pathname):  # ??
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    log = logging.getLogger("app")
    log.setLevel(logging.DEBUG)

    sth = logging.StreamHandler()
    sth.setLevel(logging.INFO)
    sth.setFormatter(formatter)
    log.addHandler(sth)

    fhnd = logging.FileHandler(pathname)
    fhnd.setLevel(logging.DEBUG)
    fhnd.setFormatter(formatter)
    log.addHandler(fhnd)
    return log


log = setup_logging('%s.log' % (sys.argv[0].split('.')[0]))  # ??


def get_session(url):
    s = requests.Session()
    s.get(url, headers=randHeader(), proxies=my_proxies)
    return s


def fetch(s, url, productID, pageNum):
    while 1:
        try:
            log.info('[crawler][fetch wait][url=%s][page=%s]', url,str(pageNum))

            data = {
                'callback': 'fetchJSON_comment98vv61',
                'productId': productID,
                'score': 0,
                'sortType': 5,
                'pageSize': 10,
                'isShadowSku': 0,
                'page': pageNum
            }

            r = s.get(url, params=data).text
            r = re.search(r'(?<=fetchJSON_comment98vv61\().*(?=\);)', r).group(0)

            subdir = 'data/review_' + str(productID)
            if not os.path.exists(subdir):
                os.mkdir(subdir)
            fopen = open(subdir + '/' + str(productID) + '_' + str(pageNum) + '.json', 'w')
            fopen.write(r)
            fopen.close()
            print 'page' + str(pageNum)
            return
        except Exception, e:
            traceback.print_exc()
            time.sleep(600)


log = setup_logging('%s.log' % (sys.argv[0].split('.')[0]))  # ??

if __name__ == '__main__':
    pageNum = 0
    #productID = 3133817  #1 iphone 7
    #productID = 1617039   #2 huawei honor
    #productID = 4110748   #3 oneplus 3t
    #productID = 3479663   #4 galaxy s7
    productID = 1217500 # iphone 6
    pageNum = 45000
    urlbase = 'http://club.jd.com/comment/productPageComments.action'
    s = requests.Session()
    # duplicates
    if os.path.exists('data/review_' + str(productID)):
        fileNames = os.listdir('data/review_' + str(productID))
    else:
        fileNames = []
    for i in range(pageNum+1):
        pageNum = i
        fname = str(productID) + '_' + str(pageNum) + '.json'
        if fname in fileNames:
            continue

        fetch(s,urlbase, productID, pageNum)
        time.sleep(30)

