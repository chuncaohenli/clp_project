#coding=utf-8
import json
import nltk
import os
import utils
import traceback

n_dict = {}
adj_dict = {}
adv_dict = {}
inverse_dict = []
posdict = []
negdict = []

################ read in all the files ##################
# comment_list = getComments(jcontent)
id_list = ['3133817']
comments = []
comments_dict = {}
allreviews_file = open('all reviews.txt', 'w')
for id in id_list:
    path =('review_3133817')
    for parent, dirnames, filenames in os.walk(path):
        for f in filenames[1:]:
            f_path = path+'/'+f
            try:
                data = utils.readJD(f_path,id)
                comments.extend(data[0])
                num_hottag = len(data[1])
            except Exception:
                traceback.print_exc()
                print f_path
                continue
for comment in comments:
    comments_dict[comment.id] = [comment.content]
    allreviews_file.write(str(comment.id) + '\t')
    allreviews_file.write((comment.content.encode('utf-8')))
    allreviews_file.write('\n')
allreviews_file.close()



n_file = open('cluster_wiki/noun_cluster_45.txt', 'r')  # input the results of noun clustering
fulltext1 = n_file.readlines()
for line in fulltext1:
    a = line.split()
    try:
        n_dict[a[1]].append(a[0])
    except KeyError:
        n_dict[a[1]] = [a[0]]
for i in n_dict.keys():
    n_dict[i] = set(n_dict[i])
n_file.close()

adj_file = open('adj_cluster(5).txt', 'r')  # input the results of adjective clustering
fulltext2 = adj_file.readlines()
for line in fulltext2:
    a = line.split()
    try:
        adj_dict[a[1]].append(a[0])
    except KeyError:
        adj_dict[a[1]] = [a[0]]
adj_file.close()
total_degrees = len(adj_dict.keys())  # describe the total number of degrees of sentiment

adv_file = open('adverb_cluster2.txt', 'r')  # input the results of adverb clustering
fulltext3 = adv_file.readlines()
for line in fulltext3:
    a = line.split()
    try:
        adv_dict[a[1]].append(a[0])
    except KeyError:
        adv_dict[a[1]] = [a[0]]
adv_file.close()
for i in adv_dict.keys():
    adv_dict[i] = set(adv_dict[i])

inverse_file = open('inverse.txt', 'r')  # input all the inverse words
fulltext6 = inverse_file.readlines()
for line in fulltext6:
    a = line.split()
    inverse_dict.append(a[0])
inverse_file.close()

posdict_file = open('posdict.txt', 'r')  # input all the inverse words
fulltext7 = posdict_file.readlines()
for line in fulltext7:
    a = line.split()
    posdict.append(a[0])
posdict_file.close()

negdict_file = open('negdict.txt', 'r')  # input all the inverse words
fulltext8 = negdict_file.readlines()
for line in fulltext8:
    a = line.split()
    negdict.append(a[0])
negdict_file.close()


def find_n_class(noun_word):
    for i in n_dict.keys():
        if noun_word in n_dict[i]:
            return(i)


def find_adj_class(adj_word):
    for i in adj_dict.keys():
        if adj_word in adj_dict[i]:
            return(i)


def find_adv_class(adv_word):
    for i in adv_dict.keys():
        if adv_word in adv_dict[i]:
            return(i)



########### capture the feature key words ###########
def capture_feature_keywords(feature_count):
    keyword = {}
    for feature_num in feature_count.keys():
        max_num = max(feature_count[feature_num].values())
        for words in feature_count[feature_num].keys():
            if feature_count[feature_num][words] == max_num:
                keyword[feature_num] = words
    return keyword
    #print json.dumps(keyword, encoding="UTF-8", ensure_ascii=False)


########### capture the degree key words ###############
def capture_senti_keywords(sentiment):
    degrees_senti = {}
    for feature_num in sentiment.keys():
        max_num = max(sentiment[feature_num].values())
        for degree in sentiment[feature_num].keys():
            if sentiment[feature_num][degree] == max_num:
                degrees_senti[feature_num] = {degree: sentiment_words[feature_num][degree][0]}
    #print('degree_senti:')
    #print json.dumps(degrees_senti, encoding="UTF-8", ensure_ascii=False)
    return degrees_senti
    #print json.dumps(feature_count, encoding="UTF-8", ensure_ascii=False)


########## output the final results ######################
def output_final(sentiment_words, keyword, degrees_senti):
    final_results = {}
    for feature_num in sentiment_words.keys():
        final_results[keyword[feature_num]] = {'degree': degrees_senti[feature_num]}
        sent_degree = degrees_senti[feature_num].keys()[0]
        final_results[keyword[feature_num]]['count'] = sentiment[feature_num][sent_degree]['count']
        final_results[keyword[feature_num]]['id'] = sentiment[feature_num][sent_degree]['id']
    #print('final_result:')
    #print json.dumps(final_results, encoding="UTF-8", ensure_ascii=False)
    output_file = open('final_result.txt', 'w')
    for i in final_results.keys():
        for j in final_results[i]['degree'].keys():
            eachline1 = i + final_results[i]['degree'][j] +\
                       '\t' + str(final_results[i]['count']) + '\t' + 'Review ID: ' + '\t'
            output_file.write(eachline1)
            subfile_name = i + final_results[i]['degree'][j] +\
                       '(' + str(final_results[i]['count']) + ')' + '.txt'
            subfile = open(subfile_name, 'w')
            for k in final_results[i]['id']:
                eachline2 = k + '\t'
                output_file.write(eachline2)
                k1 = k.split('/')[0]
                eachline3 = k1 + '\t'
                subfile.write(eachline3)
                eachline4 = comments_dict[int(k1)][0]
                subfile.write(eachline4.encode('utf-8'))
                subfile.write('\n')
            output_file.write('\n')
        subfile.close()
    output_file.close()


raw_data = {}  # store all raw data for indexing
sentiment = {}  # store all the sentiment analysis results
sentiment_words = {}  # store all the sentiment analysis results in form of words
feature_count = {}
phrases_file = open('textrank.txt', 'r')  # input all the parsing results
fulltext4 = phrases_file.readlines()
feature_keywords = []
phrases_file.close()
for line in fulltext4:  # for each feature, extract the most frequent modifier
    a = line.split( )
    feature_keywords.append(a[0])

for id in comments_dict.keys():
    review = comments_dict[id][0]
    for feature_keyword in feature_keywords:
        if feature_keyword in review.encode('utf-8'):
            try:
                sentiment[feature_keyword]['count'] += 1
                sentiment[feature_keyword]['reviews'][id] = comments_dict[id][0]
            except KeyError:
                sentiment[feature_keyword] = {'count': 1, 'reviews': {id: comments_dict[id][0]}}

final_file = open('final_textrank.txt', 'w')
for keyword in sentiment.keys():
    final_file.write(keyword + '\t' + str(sentiment[keyword]['count']) + '\n')
    subfile_name = keyword + '.txt'
    subfile = open(subfile_name, 'w')
    aa = 'count: ' + str(sentiment[keyword]['count'])
    subfile.write(aa)
    for id in sentiment[keyword]['reviews'].keys():
        eachline = '\n'+ str(id) + '\t' + sentiment[keyword]['reviews'][id].encode('utf-8')
        subfile.write(eachline)
    subfile.close()
final_file.close()
