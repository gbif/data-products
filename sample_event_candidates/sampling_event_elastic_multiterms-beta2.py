from elasticsearch6 import Elasticsearch as es
from bs4 import BeautifulSoup
import csv
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
#Parameters for the URL portion of the ElasticSearch query


def srch(body):
    #simply returns the ES search response
    res = elas.search(index="dataset", _source = ["title", "description", "_score", "samplingDescription.sampling"], _source_excludes = ["geographicCoverages"], body=body)
    #Narrows the fields looked at to the relevant ones.
    return res


def condition(term):
    '''
    Returns a construct of multiple 'should' conditions which are 'or' statements in ES
    :param terms: in our case a list of sample event/protocol terms
    :return: the construct to be inserted into the payload body to be consumed by make_body()
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

def make_body(terms):
    '''
    Create a body for ES API consumption
    terms: search terms in a multiple condition format (see https://github.com/gbif/data-products/blob/master/sample_event_candidates/Sampling_event_ElasticSearch_body_json)
    '''
    payload = {
	"_source": {
		"includes": ["title", "description", "_score", "samplingDescription"],
		"excludes": ["geographicCoverages"]
	},
	"size": 2000,

	"query": {
		"bool": {
			"should": terms }}}
    print(payload)
    return payload


dir = 'C:/Users/bxq762/Dropbox/Sample event/test/'

def remove_stopWords(wordText, custom_stop):
    #Not used initially, but is here for future development on context keywords
    words = word_tokenize(wordText)
    print('IN remove_stopwords')
    stop = set(stopwords.words('english'))
    stopped_words = [word.lower() for word in words if word.isalnum()]
    print('first stoppped :::', stopped_words)
    stopped_words = [word for word in stopped_words if word not in stop]

    return stopped_words


def clean(text, stopped=False):
    #For cleaning html and linebreaks from text strings
    #Good for free text fields

    if text:
        soup = BeautifulSoup(text, features="html.parser")
        res = soup.get_text()
        clean = re.sub(r'[^A-Za-z0-9/\. ]+', ' ', res)

        if stopped:
            #Stopword processing
            restop = remove_stopWords(res, [])
            print('¤¤¤STOPPED RESSS :::;: ', restop)
    else:
        clean = ''
    return clean


def lemmatizer(text):
    # Not used initially, but is here for future development on context keywords
    word_list = word_tokenize(text)
    lemmy = [lemma.lemmatize(w) for w in word_list]
    lem = ' '.join(lemmy)
    return lem


def run_ES_SE_search(terms):
    '''
    Simply extracts the ES search response
    :return: the metadata records themselves which are folded in at the ['hits']['hits'] level of the JSON
    '''
    conditions = condition(terms)
    body = make_body(conditions)
    res = srch(body)
    numhits = res['hits']['total']['value']
    print('&&&&&&&numhits&&&&&& : ', numhits)
    #for testing
    ore = res['hits']['hits']

    return ore


def keywordUpper(dict, keyword, text, field):
    '''
    Uppercasing keywords in the text field submitted
    :param keyword: list of protocols
    :param text: the field (title or description or samplingDescription)
    :param field: the field/column being processed
    :return: the modified field(text parameter)
    to self: MUST BE TURNED INTO A LIST-COMPREHENSION EVENTUALLY
    '''

    answer = ''
    print(dict)
    for word in keyword:
        print('TEXTT : : :', text)
        text = clean(text)
        answer = re.sub(word, word.upper(), text, flags=re.I)
        #text is keyword uppercased
        dict[field] = answer
        m = bool(re.search(r'{}'.format(word), text))
        #If the text is found with the regex search above, then the protocol term is appended to the dictionary field 'protocol_terms' (list)
        if m:
            print('in m bool- word= ', word)
            hit = word
            dict['protocol_terms'].append(hit)

    termas = dict['protocol_terms']
    protocol_terms = list(set(termas))
    #terms can be added multiple times if the term appears more than once in the text. Above turns the list into a unique list.
    dict['protocol_terms'] = protocol_terms
    return answer, dict
    #above is a tuple!!!

def mine_ore(ore, term, filename):
    '''
    Extrating the fields of interest.
    :param ore: The relevant content of the ES response
    :param term: search keyword for sampling protocol/method
    :param filename:
    :return: filename
    '''

    rowdict = {'datasetkey': '', 'title': '', 'description': '',
               'sampling': '', 'protocol_terms': [], 'score': ''}
    #This dictionary is crucial as it is being populated incrementally

    with open(dir+'/'+filename, 'w', newline='', encoding='utf-8') as sample_event_file:
        fieldnames = ['datasetkey', 'title', 'description', 'sampling', 'protocol_terms', 'score']
        #Above are headers
        writer = csv.DictWriter(sample_event_file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()

        kerrorfile = open(dir + 'key_errors-{}_{}.csv'.format(term, datetime.now().strftime('%m-%d-%Y')), 'w', newline='', encoding='utf-8')
        #When one of the text fields are empty, the output is directed into the keyerror file.

        for record in ore:
            #This is where the dictionary is being populated into an eventual row.
            rowdict = {key: 0 for key in rowdict}
            #Resetting the dictionary values so that there is no aggregation between datasets
            rowdict['protocol_terms'] = []
            datasetkey = record['_id']
            print('DATASETKEY:' , datasetkey)
            rowdict['datasetkey'] = datasetkey
            score = record['_score']
            meta_source= record['_source']
            title = meta_source['title']
            #Title is the first time we search for protocol terms.
            title = clean(title, stopped=False)
            title = keywordUpper(rowdict, term, title, 'title')
            current_dict = title[1]
            #Dictionary populated 1st time. REMEMBER that we got a tuple back from keywordUpper() - the dictionary is in position [1]

            current_dict['title'] = title[0]

            description = meta_source['description']
            description_cleaned = clean(description,stopped=False)
            description_cleaned = keywordUpper(current_dict, term, description_cleaned, 'description')
            current_dict = description_cleaned[1]
            current_dict['description'] = description_cleaned[0]
            current_dict['score'] = score
            try:
                samplingDescription = meta_source['samplingDescription']['sampling']
                if samplingDescription:
                    samplingDescription_cleaned = clean(samplingDescription, stopped=False)
                    samplingDescription_cleaned = keywordUpper(current_dict, term, samplingDescription_cleaned, 'sampling')
                    current_dict = samplingDescription_cleaned[1]
                    current_dict['sampling'] = samplingDescription_cleaned[0]

            except KeyError as e:
                #If the text field is empty in the dataset
                print('keyerror ¤¤¤¤¤¤¤¤')
                print(e)
                fieldnames = ['datasetkey', 'title', 'description', 'sampling', 'protocol_terms', 'score']
                errow = {'datasetkey': datasetkey, 'title': title[0], 'description': description_cleaned[0], 'sampling': 'Dataset contained no sampling description', 'protocol_terms': current_dict['protocol_terms'], 'score': score}

                print('ERROW ==== ', errow)
                kwriter = csv.DictWriter(kerrorfile, fieldnames=fieldnames, delimiter='\t')
                kwriter.writerow(errow)
                continue

            print('CURRR dict : ', current_dict)
            writer.writerow(
                # {'datasetkey': datasetkey, 'title': title, 'description': description_cleaned, 'sampling': samplingDescription_cleaned, 'protocol_terms': term, 'score': score}
                current_dict
            )

        return filename


# protocols = ['sampling','trap','transect','plot','survey', 'surveys','netting','census','trawl']
def run_it():
    elas = es(
        ["http://registry-search.gbif.org:9200/dataset/", "localhost:9200"])

    protocols = ['corer', 'trawl']
    #Above are the protocols being searched

    filename = 'testOCT_{}_{}2020-11-06TEST.csv'.format('Nov', 'combine')
    js = run_ES_SE_search(protocols)
    paydirt = mine_ore(js, protocols, filename)
    print(dir+paydirt)

run_it()


# DONT KNOW ABOUT THIS YET v v v
# dkeys_list = []
# def predominant_sign(data):
#     signs = Counter(k['_id'] for k in data if k.get('_id'))
#     for sign, count in signs.most_common():
#         # print(sign, count)
#         dkeys_list.append(sign)

# with open('ore.txt', 'w', encoding='utf-8') as file:
#     writer = file.write(str(ore))
#
# tally = predominant_sign(ore)
# print('key list == ', dkeys_list)
# uniq = set(dkeys_list)
# print('NUMBER of datasets with term = ', len(dkeys_list))
# print('length unique keys:: ', len(uniq))

def highlight(txt, pattern):
    '''NOT USED
    Could be used to highlight keywords in ES rather than handling it in Python. Replacement for keywordUpper()
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