from elasticsearch6 import Elasticsearch as es
from bs4 import BeautifulSoup
import csv
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
import datetime

current_date = datetime.date.today()

lemma = nltk.wordnet.WordNetLemmatizer()

elas = es(
    ["http://registry-search.gbif.org:9200/dataset/", "localhost:9200"])
#Parameters for the URL portion of the ElasticSearch query


def srch(body):
    #simply returns the ES search response
    res = elas.search(index="dataset", _source = ["title", "description", "_score", "samplingDescription.*"], _source_excludes = ["geographicCoverages"], body=body)
    #Narrows the fields looked at to the relevant ones.
    return res


def fit_query(protocols):
    """Protocols: list of singular and plural term(or other syntax) [pollard walk, pollard walks]
    Will provide escaped double quotes for the ES search body = (\"pollard walk\")" OR "(\"pollard walks\") """
    trem = r'\ "'
    output = []
    for j in protocols:
        nterm = j
        nterm = '('+trem+nterm+trem+')'
        nterm = nterm+'"'
        nterm = re.sub(r' "', '"', nterm)
        nterm = '"'+nterm
        output.append(nterm)

    return output

def make_body(protocols):
    '''
    Create a body for ES API consumption
    protocols: search terms (list) to be formatted into a single- or multiple condition format
    Returns the body for the SE search
    '''
    print('mk body. len: ', len(protocols), protocols)
    newterm_list = fit_query(protocols)
    #protocols have been fitted for ES search with "query_string"
    implant = ''
    for t in newterm_list:
        if len(implant)==0: implant = t
        else: implant = implant + ' OR ' + t
        implant = re.sub('" OR "', ' OR ', implant)

    payload = """{
  "query": {
    "bool": {
      "must": [
        {
          "query_string": {"query": """+implant+""",
            "fields": ["title", "description", "samplingDescription.sampling"]
          }}
      ]
    }
  }, "size": 200,
   "highlight": { "pre_tags": ["#"],  "post_tags": ["#"],
           "fields" : {
            "_all" : { "pre_tags" : ["<em>"], "post_tags" : ["</em>"] },
            "title" : { "number_of_fragments" : 0 },
            "description" : { "number_of_fragments" : 5 },
            "samplingDescription.sampling" : { "number_of_fragments" : 5, "order" : "score", "type" : "plain" }
        }
        }
}"""

    print(payload)
    return payload


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
        print('tyyype: ', type(text))
        soup = BeautifulSoup(text, features="html.parser")
        res = soup.get_text()
        clean = re.sub(r'[^A-Za-z0-9/\. ]+', ' ', res)

        if stopped:
            #Stopword processing
            restop = remove_stopWords(res, [])
            print('¤¤¤STOPPED RESSS :::: ', restop)
    else:
        clean = ''
    return clean


def lemmatizer(text):
    #!!!Not used initially, but is here for future development on context keywords
    word_list = word_tokenize(text)
    lemmy = [lemma.lemmatize(w) for w in word_list]
    lem = ' '.join(lemmy)
    return lem


def run_ES_SE_search(protocols):
    '''
    Simply extracts the ES search response
    :yield: the metadata records themselves which are folded in at the ['hits']['hits'] level of the JSON
    '''
    body = make_body(protocols)
    res = srch(body)
    numhits = res['hits']['total']['value']
    print('Number of search hits :: ', numhits)

    ore = res['hits']['hits']
    for nugget in ore:
        ttl = nugget['_source']['title']
        record = nugget

        yield record

# kerrorfile = open(dir + 'key_errors-{}.csv'.format(current_date, 'w',newline='', encoding='utf-8'))

SEwritefile = None
def set_writefile(filename):
    #create append ready file
    SEwritefile = open(filename, mode='a+', encoding='utf-8', newline='')
    return SEwritefile

flag = False
def mine_ore(ore, term, filename, dirr):
    '''
    Extrating the fields of interest from the ES response.
    :param ore: The relevant content of the ES response
    :param term: 'search keyword' for sampling protocol/method
    :param filename:
    :return: filename
    '''
    global flag
    #for writing the header once and only once

    sample_event_file = SEwritefile
    rowdict = {'datasetkey': '', 'title': '', 'description': '', 'sampling': [], 'protocol_terms': [], 'score': ''}
    #This dictionary is crucial as it is being populated incrementally
    if not sample_event_file:
        # print('ERRRRORRR - - - ',dirr, type(dirr), filename, type(filename))
        sample_event_file = set_writefile(dirr+filename)
        print('RETURNED SEwriteF: ', sample_event_file)
    #
    fieldnames = [*rowdict]
    #Above are headers
    print('SEwrite f: ', sample_event_file)
    writer = csv.DictWriter(sample_event_file, fieldnames=fieldnames, delimiter='\t', )
    if not flag:
        print('flag status; ', flag)
        writer.writeheader()
        flag = True
    # kerrorfile = open(dir + 'key_errors-{}_{}.csv'.format(term, datetime.now().strftime('%m-%d-%Y')), 'w', newline='', encoding='utf-8')

    rec_highlight = ore['highlight']
    if rec_highlight:
        for element in term:
            checked = regex_check_term(element, rec_highlight)
            print('CHECKED = ', checked)
            rowdict['protocol_terms'].append(checked)
        rowdict['datasetkey'] = ore['_id']
        rowdict['title'] = ore['_source']['title']
        description = clean(ore['_source']['description'])
        rowdict['description'] = description
        rowdict['score'] = ore['_score']
        print('ROWWWD: ', rowdict)
        hkeys = [*rec_highlight]
        print('hkeys: ', hkeys)
        for k in hkeys:
            if "sampl" in k:
                rowdict['sampling'].append(rec_highlight[k])

        unnested_protocols = flat_earth(rowdict['protocol_terms'])
    if unnested_protocols:
        rowdict['protocol_terms'] = unnested_protocols
        print('going into write dict: ', rowdict)
        writer.writerow(rowdict)

    return filename

def regex_check_term(term, highlight):
    '''
    Checking the ES records returned from the ES query with each of the protocols listed in term.
    # term: 'pollard walk' or 'transect'
    #highlight is the 'highlighted' text from the ES response
    '''
    opterm = []
    atoms = None
    #formatting the regex pattern
    # for j in term:
    atoms = term.split()
    print('atoms: ', atoms)
    for k in atoms:
        opterm.append('\#'+k)
    print(opterm)
    opterm = '\# '.join(opterm)
    print('new opterm', opterm+'\#')
    #END formatting the regex pattern
    # Needs added logic depending on the highlights structure
    print('---!', highlight)
    mykeys = [*highlight]
    catch = []
    for c in mykeys:
        print('mykeys :', c)
        ktext = highlight[c]
        print('ktext', ktext)
    #If field is a list, then join the list items
    if isinstance(ktext, list): jsr = ' '.join(ktext)
    print('JSR::', jsr)
    if len(catch) > 0:
        print('CATCH REAL', catch)
        caught = re.findall(opterm, jsr, flags=re.IGNORECASE)
        catch.append(caught)
    else: catch = re.findall(opterm, jsr, flags=re.IGNORECASE)
    print('CATCH', catch)
    return catch

def flat_earth(field):
    print('in FLATEARTH', field)
    flat_list = [item for sublist in field for item in sublist]
    print(flat_list)
    if flat_list:
        return flat_list[0]

def condition_ESbody_formatter(term):
    terma = term
    splat = terma.split()

    implant = r'(\"{}\") OR '
    implant_list = []
    for j in splat:
        part = implant.format(j)
        implant_list.append(part)
    jterm = '\"'.join(implant_list)
    rterm = re.sub(' OR $', '', jterm)
    print(rterm, 'aaaaaaaaaaaaaaaa')
    return rterm

# protocols = ['sampling','trap','transect','plot','survey', 'surveys','netting','census','trawl']
def run_it(directory, protocols):
    '''
    #Remember to add the plural/participle  term to the protocol/terms list if relevant. That creates the body with ' OR ' condition
    '''

    print('in run_it()', protocols)
    # protocols = ['corer', 'netting', 'quadrat']
    #Above are the protocols being searched
    filename = 'test_{}_{}{}TEST.csv'.format('June', protocols[0].replace(" ",""), current_date)
    record_gen = run_ES_SE_search(protocols)
    print('øøø', record_gen, 'øøø')
    # writest = open('ESHits.txt', mode='w')
    # writest.write(json.dumps(js))

    # filepath = directory+filename
    for record in record_gen:
        print('yyyyyyyyyy', record)
        # break
        paydirt = mine_ore(record, protocols, filename, directory)
        print(directory+paydirt)

