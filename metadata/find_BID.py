import json
import re
import requests
import pandas as pd


def find_BID_dataset_per_country(country, step):
    '''
    For a given country, returns a list of dataset keys with a valid BID id
    '''
    dataset_with_BID_id = []
    end = False
    offset = 0
    while not end:
        param = {
            "publishingCountry": country,
            "offset": offset,
            "limit": step
        }
        dataset_list = requests.get("http://api.gbif.org/v1/dataset/search", param)
        dataset_list = dataset_list.json()
        for dataset in dataset_list["results"]:
            if "projectIdentifier" in dataset:
                if is_BID(dataset["projectIdentifier"]):
                    dataset_with_BID_id.append(dataset["key"])
        end = dataset_list["endOfRecords"]
        offset += step
    return dataset_with_BID_id


def is_BID(project_id):
    '''
    Check if string is a valid BID identifier
    '''
    isbid = False
    bid = re.match(r'^BID-((AF)|(PA)|(CA))20\d{2}-\d{4}-((REG)|(NAC)|(SMA))', project_id, flags=0)
    if bid is not None:
        isbid = True
    return isbid
