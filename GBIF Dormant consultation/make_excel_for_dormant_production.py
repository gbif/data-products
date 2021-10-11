# Purpose: Build a fundamental excel file for MS Power Automate mail merger based on the non-publishing orgs API https://api.gbif.org/v1/organization/nonPublishing
#Keys of interest can be chosen from the json response
#The processed dictionary flat file will be written to a Pandas table. 
# This data frame table will be used to calculate years-since-registration and filtering out publishers that are actually hosting resources. 

from tabulate import tabulate
import requests
import csv
import pandas
import json
import numpy
import datetime


delivery = []
#List to be populated by the api_dormant function. Delivery will be returned
# upon the 'end_of_records' response being True
# dormants = []
def api_dormant(url, offset, limit=500):
    '''Recursive function where the web content JSON is collected'''
    #url: a url string with var placeholder, like "https://api.gbif.org/v1/organization/nonPublishing?limit=200&offset={}"
    #offset is the incrementor for paging.
    #Limit holds the size of the JSON response.
    #Returns the function recursively until the condition ['endOfRecords'] is reached.
    nurl = url.format(limit)
    print('the new url : ', nurl)
    resp = requests.get(nurl)
    spons = json.loads(resp.text)
    jresp = spons['results']
    # print(jresp)
    return jresp
    #the JSON we areinterested in
    # dormants.append(jresp)
    # print('endrecs bool: ', spons['endOfRecords'])
    # if spons['endOfRecords']:
    #     return dormants
    # print('no end yet, hombre')
    # noffset = spons['offset'] + limit
    #The neat thing here is that by adding 'offset' and 'limit', it is impossible to jump ahead and miss records (results)
    # return api_dormant(url, noffset, limit)

def get_contacts(contacts):
    # get the contacts from the api call into ONE dictionary
    processed_contacts = []
    standard_contact_dict = {'firstName':'', 'lastName':'', 'email':''}
    for item in contacts:

        # make unique keys in each contact dict
        tpe = item['type'].split('_', maxsplit=1)

        fname = item.get('firstName', '')
        lname = item.get('lastName', '')
        email = item.get('email', '')
        contact_list = [fname, lname, email]
        standard_contact_dict.update(zip(standard_contact_dict, contact_list))
        # individual = {k: item[k] for k in ('firstName', 'lastName', 'email')}
        # truncate the no. of contact fields
        for key in standard_contact_dict:
            if isinstance(standard_contact_dict[key], list):
                # extract content in case the value is a list
                standard_contact_dict[key] = ''.join(standard_contact_dict[key])
        if tpe[0] == 'ADMINISTRATIVE':
            processed_contacts.append(dict(("{} {}".format(tpe[0], k), v) for k, v in standard_contact_dict.items()))
            #one liner for making a dict going into the processed contacts list
        elif tpe[0] == 'TECHNICAL':
            processed_contacts.append(dict(("{} {}".format(tpe[0], k), v) for k, v in standard_contact_dict.items()))
        elif tpe[0] == 'POINT':
            processed_contacts.append(dict(("{} {}".format(tpe[0], k), v) for k, v in standard_contact_dict.items()))

    return processed_contacts

def mk_dicts_of_nonpublishing_api():
    resp = api_dormant('https://api.gbif.org/v1/organization/nonPublishing?limit={}', 0)
    # feed = resp[0]

    for dct in resp:
        contacts = dct['contacts']
        #grab the contacts list in the json response
        contacts_as_dict = get_contacts(contacts)
        res_contacts = {k: v for x in contacts_as_dict for k, v in x.items()}
        #concatenate dictionaries ; we want everything on ONE line!
        try:
            left_part_dict = {k: dct[k] for k in ('key', 'endorsingNodeKey', 'endorsementStatus', 'title', 'country', 'created')}
        except KeyError:
            print('keyerrrrrrrrrrror ::' , dct['key'])
            continue
        print('left dict:', left_part_dict)
        # this dict contains the publisher information. There will be a middle part (contacts) and the node manager part, then an end part (difference in years)
        pub_contacts = {**left_part_dict, **res_contacts}
        # Add the pub dict and contacts dict together (like railway coupling)

        node_uuid = pub_contacts['endorsingNodeKey']
        node_manager = get_node_manager(node_uuid)

        complete_row = {**pub_contacts, **node_manager}
        delivery.append(complete_row)
    return delivery

def get_node_manager(uuid):
    node_api = 'https://api.gbif.org/v1/node/{}'.format(uuid)
    resp = requests.get(node_api)
    spons = json.loads(resp.text)
    node_title = spons['title']
    jresp = spons['contacts']
    node_manager = {'node': '', 'node_manager': '', 'manager_email': ''}

    for k in jresp:
        try:
            if k['type'] == 'NODE_MANAGER':
                name = k['firstName']+' '+k['lastName']

                # extract content in case the value is a list
                email = ''.join(k['email'])
                node_manager = {'node': node_title, 'node_manager': name, 'manager_email': email}
        except KeyError:
            continue
            #
    # print('type? ', type(node_manager), node_manager)
    return node_manager
#
def calc_difference_between_registration_date_and_now(df):
    # param df: The data frame = df_for_excel
    print('TEST created... ', df.head().to_string )
    right_now = datetime.datetime.now()
    right_now = right_now.replace(tzinfo=None)
    # sanetize time zone data to prepare for the subtraction below
    df.created = pandas.to_datetime(df['created']).dt.tz_convert(None)
    #extract one column (publisher registration date)
    diff = (right_now - df.created)

    delta = diff / numpy.timedelta64(1, 'Y')
    # get the difference in years

    delta = delta.to_frame('diff_years')
    # convert column to data frame format
    df_with_delta = pandas.concat([df, delta], axis=1)
    #tag the diff column to the end of the excel ready data frame
    return df_with_delta

def identify_hosting_publishers(uuids):
    #find the organizations that are in fact hosting datasets even though they themselves are not publishing
    #param: uuids , are all org keys in the df_candidate data frame
    api_url = 'https://api.gbif.org/v1/organization/{}/hostedDataset'
    hosting_list= []
    for j in uuids:
        call_url = api_url.format(j)
        response = requests.get(call_url)
        jresp = json.loads(response.text)
        count = jresp['count']
        if count > 0:
            hosting_list.append(j)
    return hosting_list

#!! start EXE part: -v
dicts_for_DF = mk_dicts_of_nonpublishing_api()
#list of dicts

df_candidate = pandas.DataFrame(dicts_for_DF)

orgs_list = df_candidate['key'].tolist()

hosting_pubs = identify_hosting_publishers(orgs_list)

cleaned_df_for_excel = df_candidate[~df_candidate['key'].isin(hosting_pubs)]

# #below can be used for further test operations with read_pickle()
# df_for_excel.to_excel('test_created_field2.xlsx')
# df_for_excel.to_pickle("./original_df.pkl")
# #end pickle
final_df = calc_difference_between_registration_date_and_now(cleaned_df_for_excel)
print('final df length: ', final_df.shape[0])

gt3years_df = final_df[final_df.diff_years >= 3]
print('gt3years df length: ', gt3years_df.shape[0])
prod_df = gt3years_df[gt3years_df.endorsementStatus == 'ENDORSED']

prod_df.to_excel('your_excel_file_path.xlsx', index=False)
## \ end of EXE part
