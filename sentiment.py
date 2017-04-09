#coding=utf-8
import json
import nltk

n_dict = {}
adj_dict = {}
adv_dict = {}
inverse_dict = []
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


raw_data = {}  # store all raw data for indexing
sentiment = {}  # store all the sentiment analysis results
sentiment_words = {}  # store all the sentiment analysis results in form of words
feature_count = {}
phrases_file = open('parsing.txt', 'r')
fulltext4 = phrases_file.readlines()
for line in fulltext4:
    a = line.split()
    id = a[0]
    raw_data[a[0]] = line.lstrip(a[0]).lstrip(' ')  # store the raw data
    noun_word = a[1]
    n_class = find_n_class(noun_word)
    try:
        feature_count[n_class][noun_word] += 1
    except KeyError:
        try:
            feature_count[n_class][noun_word] = 1
        except KeyError:
            feature_count[n_class] = {noun_word: 1}
    if len(a) == 4:
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

        try:
            sentiment[n_class][degree] += 1
            sentiment_words[n_class][degree].append(adj_word)
        except KeyError:
            try:
                sentiment[n_class][degree] = 1
                sentiment_words[n_class][degree] = [adj_word]
            except KeyError:
                sentiment[n_class]={degree: 1}
                sentiment_words[n_class] = {degree: [adj_word]}

    elif len(a) == 3:
        adj_word = a[2]
        adj_class = find_adj_class(adj_word)
        if adj_class == None:
            degree = 2
        else:
            degree = adj_class
        try:
            sentiment[n_class][degree] += 1
            sentiment_words[n_class][degree].append(adj_word)
        except KeyError:
            try:
                sentiment[n_class][degree] = 1
                sentiment_words[n_class][degree] = [adj_word]
            except KeyError:
                sentiment[n_class]={degree: 1}
                sentiment_words[n_class] = {degree: [adj_word]}

#print('sentiment:', sentiment)
#print json.dumps(sentiment_words, encoding="UTF-8", ensure_ascii=False)
phrases_file.close()
for noun_class in sentiment.keys():
    class_degree = max(sentiment[noun_class])
#print('adj_dict:')
#print json.dumps(adj_dict, encoding="UTF-8", ensure_ascii=False)

########### capture the feature key words ###########
keyword = {}
max_num = 0
for feature_num in feature_count.keys():
    max_num = max(feature_count[feature_num].values())
    for words in feature_count[feature_num].keys():
        if feature_count[feature_num][words] == max_num:
            keyword[feature_num] = words
#print json.dumps(keyword, encoding="UTF-8", ensure_ascii=False)


########### capture the degree key words ###############
degrees_senti = {}
max_num = 0
for feature_num in sentiment.keys():
    max_num = max(sentiment[feature_num].values())
    for degree in sentiment[feature_num].keys():
        if sentiment[feature_num][degree] == max_num:
            degrees_senti[feature_num] = {degree: sentiment_words[feature_num][degree][0]}
#print json.dumps(degrees_senti, encoding="UTF-8", ensure_ascii=False)
#print json.dumps(feature_count, encoding="UTF-8", ensure_ascii=False)


########## output the final results ######################
final_results = {}
for feature_num in sentiment_words.keys():
    final_results[keyword[feature_num]] = degrees_senti[feature_num]
#print json.dumps(final_results, encoding="UTF-8", ensure_ascii=False)
output_file = open('final_result.txt', 'w')
for i in final_results.keys():
    for j in final_results[i].keys():
        eachline = i + final_results[i][j] + '\t' + 'sentiment degree: ' + '\t' + j + '\n'
        output_file.write(eachline)
output_file.close()