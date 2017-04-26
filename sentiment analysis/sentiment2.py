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



n_file = open('noun_cluster.txt', 'r')  # input the results of noun clustering
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

adj_file = open('adj_cluster.txt', 'r')  # input the results of adjective clustering
fulltext2 = adj_file.readlines()
for line in fulltext2:
    a = line.split()
    try:
        adj_dict[a[1]].append(a[0])
    except KeyError:
        adj_dict[a[1]] = [a[0]]
adj_file.close()
total_degrees = len(adj_dict.keys())  # describe the total number of degrees of sentiment

adv_file = open('adverb_cluster.txt', 'r')  # input the results of adverb clustering
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
                       '(' + str(final_results[i]['count']) + ')' + '\t' + 'Review ID: ' + '\t'
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
phrases_file = open('parsing4.txt', 'r')  # input all the parsing results
fulltext4 = phrases_file.readlines()
for line in fulltext4:
    a = line.split( )
    id = a[0]
    raw_data[a[0]] = line.lstrip(a[0]).split()  # store the raw data
    noun_word = a[1]
    n_class = find_n_class(noun_word)
    try:
        feature_count[n_class][noun_word] += 1
    except KeyError:
        try:
            feature_count[n_class][noun_word] = 1
        except KeyError:
            feature_count[n_class] = {noun_word: 1}
    if len(a) == 4:  # there is an adv before the adj
        adj_word = a[3]
        adv_word = a[2]
        adj_class = find_adj_class(adj_word)
        adv_class = find_adv_class(adv_word)
        if adj_class == None:
            degree = 2
        else:
            degree = adj_class

        if adv_word in inverse_dict:  # check inverse words
            degree = str(0 - int(degree))
            addvalues = adv_word + adj_word
            try:
                adj_dict[degree].append(addvalues)
            except KeyError:
                adj_dict[degree] = [addvalues]
        else:
            addvalues = adj_word

        try:
            sentiment[n_class][degree]['count'] += 1
            sentiment[n_class][degree]['id'].append(id)
            sentiment_words[n_class][degree].append(addvalues)
        except KeyError:
            try:
                sentiment[n_class][degree]['count'] = 1
                sentiment[n_class][degree]['id'] = [id]
                sentiment_words[n_class][degree] = [addvalues]
            except KeyError:
                try:
                    sentiment[n_class][degree] = {'count': 1, 'id': [id]}
                    sentiment_words[n_class][degree] = [addvalues]
                except KeyError:
                    sentiment[n_class]={degree: {'count':1, 'id': [id]}}
                    sentiment_words[n_class] = {degree: [addvalues]}

    elif len(a) == 3:  # if there is no adv
        adj_word = a[2]
        adj_class = find_adj_class(adj_word)
        if adj_class == None:
            degree = 2
        else:
            degree = adj_class
        try:
            sentiment[n_class][degree]['count'] += 1
            sentiment[n_class][degree]['id'].append(id)
            sentiment_words[n_class][degree].append(adj_word)
        except KeyError:
            try:
                sentiment[n_class][degree]['count'] = 1
                sentiment[n_class][degree]['id'] = [id]
                sentiment_words[n_class][degree] = [adj_word]
            except KeyError:
                try:
                    sentiment[n_class][degree] = {'count': 1, 'id': [id]}
                    sentiment_words[n_class][degree] = [adj_word]
                except KeyError:
                    sentiment[n_class] = {degree: {'count': 1, 'id': [id]}}
                    sentiment_words[n_class] = {degree: [adj_word]}

#print('sentiment:')
#print(sentiment)
#print('sentiment_word:')
#print json.dumps(sentiment_words, encoding="UTF-8", ensure_ascii=False)
phrases_file.close()
for noun_class in sentiment.keys():
    class_degree = max(sentiment[noun_class])
#print('adj_dict:')
#print json.dumps(adj_dict, encoding="UTF-8", ensure_ascii=False)
feature_keywords = capture_feature_keywords(feature_count)
degrees_senti = capture_senti_keywords(sentiment)
output_final(sentiment_words, feature_keywords, degrees_senti)