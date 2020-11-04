from elasticsearch6 import Elasticsearch as es
from bs4 import BeautifulSoup
import csv
import json
from collections import Counter
from datetime import datetime

import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

lemma = nltk.wordnet.WordNetLemmatizer()
elas = es(
    ["http://registry-search.gbif.org:9200/dataset/", "localhost:9200"])


# print(es.info())

def srch(body):
    #simply returns the ES search response
    res = elas.search(index="dataset", _source = ["title", "description", "_score", "samplingDescription.sampling"], _source_excludes = ["geographicCoverages"], body=body)
    return res


def condition(term):
    '''
    Returns a construct of multiple 'should' conditions whcih are 'or' statements in ES
    :param terms: in our case a list of sample event/protocol terms
    :return: the construct to be inserted into the payload body
    '''
    fields = ['title', 'description', 'samplingDescription']
    shoulds = []
    for item in term:
        for f in fields:
            should = {
                        "wildcard": {
                            f: {
                                "value": "{}?".format(item),
                                "rewrite": "scoring_boolean"
                            }
                        }
                    }
            # should = shoulds.replace("'", '"')
            shoulds.append(should)
    return shoulds

def make_body(term):
    '''
    Create a body for ES API consumption
    conditions: search terms
    '''
    payload = {
	"_source": {
		"includes": ["title", "description", "_score", "samplingDescription"],
		"excludes": ["geographicCoverages"]
	},
	"size": 2000,

	"query": {
		"bool": {
			"should": term }}}
    return payload


dir = r'C:/Users/bxq762/Dropbox/Sample event/'

def remove_stopWords(wordText, custom_stop):
    words = word_tokenize(wordText)
    print('IN remove_stopwords')
    stop = set(stopwords.words('english'))
    stopped_words = [word.lower() for word in words if word.isalnum()]
    print('first stoppped :::', stopped_words)
    stopped_words = [word for word in stopped_words if word not in stop]

    # print(type(stopped_words), stopped_words)
    return stopped_words
    # words = word_tokenize(stopped_text)
    # filtered = [word for word in stopped_words if word not in custom_stop]
    # return filtered


def clean(description_text, stopped=True):
    #For cleaning html and linebreaks from text strings
    #Good for keyword and free text fields
    print('desc text yooooooo : ', description_text)
    if description_text:
        soup = BeautifulSoup(description_text, features="html.parser")
        res = soup.get_text()
        # print('#########soup res === ', res)
        if stopped:
            restop = remove_stopWords(res, [])
            print('¤¤¤STOPPED RESSS :::;: ', restop)
    # tmp = restop.split()
            cleaned = ' '.join(restop)
        else:
            print('inside FALSE')
            cleaned = re.sub(r'\W+', ' ', res)
            # cleaned = res.replace("\n", "")
            # cleaned = cleaned.replace("\r", "")
            print('CLEAN() --- ', cleaned, 'end clean()')
    else:
        cleaned = ''
    return cleaned


def highlight(txt, pattern):
    '''
    Gets the results of the highlighted text.
    :param txt: text to be searched
    :param pattern: regex pattern
    :return: a list of terms that were matched for a particular string
    '''
    print('txt =={} \n and pattern : {}'.format(txt, pattern))
    matched = []

    fields = ['description']
    print('txt type is : ', type(txt), '  ', txt)
    print(txt)
    item_list = [txt[x] for x in fields]
    item_list_conc = item_list[0]
    one_list = '. '.join(item_list_conc)
    print('ITEM LIST here = ',len(one_list), type(one_list), one_list)

    print('mathced texxxxxtttt: len: {} + text: {}'.format(len(one_list), one_list))
    hit = re.findall(pattern, one_list)
    hit = [x.lower() for x in hit]
    print('#hit##', hit)
    matched.append(hit)
    print('type matched?? : ', type(matched), matched)

    res = list(set(matched[0]))
    #Set returns a unique 'set' which must be cast as list
    return res


def lemmatizer(text):
    word_list = word_tokenize(text)
    lemmy = [lemma.lemmatize(w) for w in word_list]
    lem = ' '.join(lemmy)
    return lem


def run_ES_SE_search(filename, term):
    conditions = condition(term)
    body = make_body(conditions)
    res = srch(body)
    numhits = res['hits']['total']['value']
    print('&&&&&&&numhits&&&&&& : ', numhits)
    ore = res['hits']['hits']

    return ore


def mine_ore(ore, term, filename):
    '''
    Extrating the fields of interest.
    :param ore: The relevant content of the ES response
    :param term: search keyword for sampling protocol/method
    :param filename:
    :return: filename
    '''
    def keywordUpper(keyword, text):
        '''
        Uppercasing keywords
        :param keyword: list of protocols
        :param text: the field (title or description or samplingDescription)
        :return: the modified field(text parameter)
        MUST BE TURNED INTO A LIST-COMPREHENSION
        '''
        if isinstance(keyword, list):
            kiter = iter(keyword)
            item = next(kiter)

            last = keyword[-1]
            if text:
                subbed = re.sub(item, item.upper(), text)
                print('inside if text: ', subbed)
                item = next(kiter)
                if item == last:
                    print('{} AND {}'.format(item, last))
                    subbed = re.sub(item, item.upper(), subbed)
                    return subbed

    with open(dir+'/'+filename, 'w', newline='', encoding='utf-8') as sample_event_file:
        fieldnames = ['datasetkey', 'title', 'description', 'sampling', 'protocol_terms', 'score']
        writer = csv.DictWriter(sample_event_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        textlist = []
        def nuggets(key, value):
            tdict = dict()
            tdict[key] = value
            textlist.append(tdict)
            yield textlist

        kerrorfile = open(dir + 'key_errors-{}_{}.csv'.format(term, datetime.now().strftime('%m-%d-%Y')), 'w', newline='', encoding='utf-8')
        for gold in ore:
            # print('gold ### =',type(gold), gold)
            datasetkey = gold['_id']
            nuggets('datasetkey', datasetkey)
            score = gold['_score']
            nuggets('score', score)
            gold_source= gold['_source']
            # print('gold ### =',type(gold_source), gold_source)
            title = gold_source['title']
            ltitle = lemmatizer(title)
            nuggets('title', ltitle)
            title = clean(title, stopped=False)

            title = keywordUpper(term, title)
            description = gold_source['description']
            description_cleaned = clean(description,stopped=False)
            description_cleaned = keywordUpper(term, description_cleaned)
            print('DESC CLEANED and subbed: ', description_cleaned)
            nuggets('description', description_cleaned)
            print('D#D#D#D#D#  ', description_cleaned, '\n¤¤¤¤¤¤¤¤¤ ', description)
            description = keywordUpper(term, description_cleaned)
            try:
                # hl = highlight(gold, pattern, ['highlight', 'description'])
                # print('HIGHLIGHT¤¤¤¤¤:', hl)
                samplingDescription = gold_source['samplingDescription']['sampling']
                if samplingDescription:
                    # print('SSAAMMPPLLIINNGG !!!!! : ', samplingDescription)
                    # break
                    samplingDescription_cleaned = clean(samplingDescription, stopped=False)
                    samplingDescription_cleaned = keywordUpper(term, samplingDescription_cleaned)
                    nuggets('sampling', samplingDescription_cleaned)
                    print('cccleaned SAMPLING:::: ', samplingDescription_cleaned)
                    print(type(samplingDescription))
                    # break
            except KeyError as e:
                #rewrite to match format of the writerow()
                print('keyerror ¤¤¤¤¤¤¤¤')
                print(e)
                fieldnames_error = ['_id', '_score', '_source']
                # errow = {'_id': gold['_id'], '_score': gold['_score'], '_source': gold['_source']}
                fieldnames = ['datasetkey', 'title', 'description', 'sampling', 'protocol_terms', 'score']
                errow = {'datasetkey': datasetkey, 'title': title, 'description': description_cleaned, 'sampling': 'Dataset contained no sampling description', 'protocol_terms': term, 'score': score}
                # keys = gold.keys()
                print('ERROW ==== ', errow)
                kwriter = csv.DictWriter(kerrorfile, fieldnames=fieldnames, delimiter='\t')
                kwriter.writerow(errow)
                # break
                continue
            # title = clean(title)
            # term_lights = re.sub(term, term.upper(), title)
            print("#TITLE ::: ", ltitle)
            print('##desc##: ', description_cleaned)

            print('type orig description: ', type(description))
            print('going to write: datasetkey: {}, title: {}, description_cleaned: {}, sampling: {}, protocol_terms: {}, score: {} '.format(
                datasetkey, title, description_cleaned, samplingDescription, term, score))
            writer.writerow(
                {'datasetkey': datasetkey, 'title': title, 'description': description_cleaned, 'sampling': samplingDescription_cleaned, 'protocol_terms': term, 'score': score})
            #break return!!!!!!!
            return filename


# protocols = ['sampling','trap','transect','plot','survey', 'surveys','netting','census','trawl']
def run_it():
    elas = es(
        ["http://registry-search.gbif.org:9200/dataset/", "localhost:9200"])
    # print(es.info())
    protocols = ['plot', 'trap']
    lemma = nltk.wordnet.WordNetLemmatizer()
    filename = 'testOCT_{}_{}2020-11-04FIN.csv'.format('Nov', 'combine')
    js = run_ES_SE_search(filename, protocols)
    fin = mine_ore(js, protocols, filename)

run_it()








# DONT KNOW ABOUT THIS YET v v v
# dkeys_list = []
# def predominant_sign(data):
#     signs = Counter(k['_id'] for k in data if k.get('_id'))
#     for sign, count in signs.most_common():
#         # print(sign, count)
#         dkeys_list.append(sign)

# with open('ore.txt', 'w', encoding='utf-8') as flie:
#     writer = flie.write(str(ore))
#
# tally = predominant_sign(ore)
# print('key list == ', dkeys_list)
# uniq = set(dkeys_list)
# print('NUMBER of datasets with term = ', len(dkeys_list))
# print('length unique keys:: ', len(uniq))