import json
import time
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_metadata_from_API(sample_datasets=None, exclude=None, step=300):
    '''
    Get the infor we want to monitor
    '''
    fields_of_interest = ["type",
                          "title_len",
                          "has_description",
                          "has_purpose",
                          "has_adm_or_metadata_contact",
                          "has_adm_or_metadata_contact_email",
                          "has_geographic_descrition",
                          "has_bounding_box",
                          "has_taxonomy",
                          "number_of_dates",
                          "has_qualityControl",
                          "has_studyExtent",
                          "has_sampling",
                          "has_methodSteps"]
    minimun_title_len = 3
    summary_metadata = pd.DataFrame(columns=fields_of_interest)
    if sample_datasets is not None:

        for uuid in sample_datasets:
            response = requests.get("http://api.gbif.org/v1/dataset/"+uuid)
            if response.ok:
                response = response.json()
                summary_metadata = update_dataframe(summary_metadata, uuid, response)
                summary_metadata = update_summary_with_scores(summary_metadata, uuid, minimun_title_len)
            else:
                print("NOT OK: ", uuid)
    else: 
        offset = 0
        end_of_records = False
        while not end_of_records:
            param = {
                "offset": offset,
                "limit": step
            }
            response = requests.get("http://api.gbif.org/v1/dataset", param)
            response = response.json()
            for dataset in response["results"]:
                if exclude is not None:
                    if dataset["publishingOrganizationKey"] not in exclude:
                        summary_metadata = update_dataframe(summary_metadata, dataset["key"], dataset)
                        summary_metadata = update_summary_with_scores(summary_metadata, dataset["key"], minimun_title_len)
                else:
                    summary_metadata = update_dataframe(summary_metadata, dataset["key"], dataset)
                    summary_metadata = update_summary_with_scores(summary_metadata, dataset["key"], minimun_title_len)
            time.sleep(1)
            offset += step
            end_of_records = response["endOfRecords"]

    return summary_metadata


def get_metadata_from_API_one_country(country, step=300):
    '''
    Get the info we want to monitor for one country
    '''
    return get_metadata_from_API(get_uuid_datasets_one_country(country, step))


def get_uuid_datasets_one_country(country, step):
    '''
    Get the list of datasets published by one country
    '''
    return get_uuid_datasets_one_variable("publishingCountry", country, step)


def get_uuid_datasets_one_publisher(org_uuid, step):
    '''
    Get the list of datasets published by one organization
    '''
    return get_uuid_datasets_one_variable("publishingOrg", org_uuid, step)


def get_uuid_datasets_one_variable(varname, varvalue, step):
    '''
    Get the list of datasets published by one variable
    '''
    return get_info_dataset_one_variable("key", varname, varvalue, step)


def get_uuid_organizations_one_country(country, step):
    '''
    Get the list of datasets published by one variable
    '''
    return list(set(get_info_dataset_one_variable("publishingOrganizationKey",
                                                  "publishingCountry",
                                                  country,
                                                  step)))


def get_info_dataset_one_variable(info, varname, varvalue, step):
    '''
    Infor must be the key of an element available from the API
    '''
    offset = 0
    dataset_list = []
    limit = offset + step
    end_of_records = False
    while not end_of_records:
        param = {
            varname: varvalue,
            "offset": offset,
            "limit": limit
        }
        response = requests.get("http://api.gbif.org/v1/dataset/search", param)
        if response.ok:
            response = response.json()
            for dataset in response["results"]:
                if info in dataset:
                    dataset_list.append(dataset[info])
            time.sleep(1)
            offset += step
            end_of_records = response["endOfRecords"]
        else:
            end_of_records = True
    return dataset_list


def update_dataframe(summary_metadata, uuid, response):
    '''
    Update all columns dataset for a given row
    '''

    # GLOBAL
    summary_metadata = update_dataframe_general_metadata(summary_metadata, uuid, response)

    # PURPOSE
    summary_metadata = update_dataframe_pupose_metadata(summary_metadata, uuid, response)

    # CONTACTS
    summary_metadata = update_dataframe_contact_metadata(summary_metadata, uuid, response)

    # TAXONOMY
    summary_metadata = update_dataframe_taxonomy_metadata(summary_metadata, uuid, response)

    # GEOGRAPHY
    summary_metadata = update_dataframe_geography_metadata(summary_metadata, uuid, response)

    # TIME
    summary_metadata = update_dataframe_time_metadata(summary_metadata, uuid, response)

    # METHOD
    summary_metadata = update_dataframe_method_metadata(summary_metadata, uuid, response)

    return summary_metadata


def update_dataframe_general_metadata(summary_metadata, uuid, response):
    '''
    Update general metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "type"] = response["type"]
    summary_metadata.at[uuid, "has_description"] = False
    if "title" in response:
        summary_metadata.at[uuid, "title_len"] = len(response["title"].split(" "))
    else:
        summary_metadata.at[uuid, "title_len"] = 0.0
    if "description" in response:
        if response["description"]:
            summary_metadata.at[uuid, "has_description"] = True
    return summary_metadata



def update_dataframe_pupose_metadata(summary_metadata, uuid, response):
    '''
    Update purpose metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "has_purpose"] = False
    if "purpose" in response:
        summary_metadata.at[uuid, "has_purpose"] = True
    return summary_metadata



def update_dataframe_contact_metadata(summary_metadata, uuid, response):
    '''
    Update contact metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "has_adm_or_metadata_contact"] = False
    summary_metadata.at[uuid, "has_adm_or_metadata_contact_email"] = False
    if "contacts" in response:
        for ind in response["contacts"]:
            if "type" in ind:
                if ind["type"] == "ADMINISTRATIVE_POINT_OF_CONTACT" or ind["type"] == "METADATA_AUTHOR":
                    summary_metadata.at[uuid, "has_adm_or_metadata_contact"] = True
                if "email" in ind:
                    summary_metadata.at[uuid, "has_adm_or_metadata_contact_email"] = True
    return summary_metadata


def update_dataframe_geography_metadata(summary_metadata, uuid, response):
    '''
    Update geography metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "has_geographic_descrition"] = False
    summary_metadata.at[uuid, "has_bounding_box"] = False
    if "geographicCoverages" in response:
        for geo in response["geographicCoverages"]:
            if "description" in geo:
                if geo["description"]:
                    summary_metadata.at[uuid, "has_geographic_descrition"] = True
            if "boundingBox" in geo:
                if len(geo["boundingBox"].keys()) > 1:
                    summary_metadata.at[uuid, "has_bounding_box"] = True
    return summary_metadata


def update_dataframe_taxonomy_metadata(summary_metadata, uuid, response):
    '''
    Update taxonomy metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "has_taxonomy"] = False
    if "taxonomicCoverages" in response:
        if len(response["taxonomicCoverages"]) >= 1:
            summary_metadata.at[uuid, "has_taxonomy"] = True
    return summary_metadata


def update_dataframe_time_metadata(summary_metadata, uuid, response):
    '''
    Update time metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "number_of_dates"] = 0.0
    if "temporalCoverages" in response:
        for time_coverage in response["temporalCoverages"]:
            type_temporal_coverage = 0.0
            if "@type" in time_coverage:
                type_temporal_coverage += 1
            if "type" in time_coverage:
                type_temporal_coverage += 1
            summary_metadata.at[uuid, "number_of_dates"] += (len(time_coverage)-type_temporal_coverage)
    return summary_metadata


def update_dataframe_method_metadata(summary_metadata, uuid, response):
    '''
    Update project method columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "has_qualityControl"] = False
    summary_metadata.at[uuid, "has_studyExtent"] = False
    summary_metadata.at[uuid, "has_sampling"] = False
    summary_metadata.at[uuid, "has_methodSteps"] = False
    if "samplingDescription" in response.keys():
        for para_title in response["samplingDescription"]:
            if para_title == "qualityControl":
                summary_metadata.at[uuid, "has_qualityControl"] = True
            elif para_title == "studyExtent":
                summary_metadata.at[uuid, "has_studyExtent"] = True
            elif para_title == "sampling":
                summary_metadata.at[uuid, "has_sampling"] = True
            elif para_title == "methodSteps":
                summary_metadata.at[uuid, "has_methodSteps"] = True
    return summary_metadata


def count_categories(my_summary, variable_of_interest, label_for_zero_count):
    '''
    Counts items in list in a given column
    '''
    all_type = pd.Series(my_summary[variable_of_interest].sum()).value_counts()
    my_type = all_type.append(pd.Series(len([my_summary[my_summary[variable_of_interest].apply(len) == 0]]),
                                        index=[label_for_zero_count]))
    return my_type


def update_summary_with_scores(summary_metadata, uuid, minimun_title_len):
    '''
    Caluclate score for everything and update summary
    '''
    summary_metadata.at[uuid, "score_what"] = score_general_parameters(summary_metadata, uuid, minimun_title_len)
    summary_metadata.at[uuid, "score_what"] += score_taxonomy(summary_metadata, uuid)
    summary_metadata.at[uuid, "score_why"] = score_purpose(summary_metadata, uuid)
    summary_metadata.at[uuid, "score_who"] = score_email(summary_metadata, uuid)
    summary_metadata.at[uuid, "score_where"] = score_geographic_coverage(summary_metadata, uuid)
    summary_metadata.at[uuid, "score_when"] = score_time_coverage(summary_metadata, uuid)
    summary_metadata.at[uuid, "score_how"] = score_method(summary_metadata, uuid)
    return summary_metadata


def score_general_parameters(summary_metadata, uuid, minimun_title_len):
    '''
    Calculate quality score for title and general description
    '''
    score = 0
    if summary_metadata.loc[uuid, "title_len"] > 0 or summary_metadata.loc[uuid, "has_description"]:
        score += 1
    if summary_metadata.loc[uuid, "title_len"] >= minimun_title_len:
        score += 1
    return score


def score_taxonomy(summary_metadata, uuid):
    '''
    Calculate quality score for taxonomy
    '''
    score = 0
    if summary_metadata.loc[uuid, "has_taxonomy"]:
        score += 1
    return score


def score_purpose(summary_metadata, uuid):
    '''
    Calculate quality score for purpose
    '''
    score = 0
    if summary_metadata.loc[uuid, "has_purpose"]:
        score += 1
    return score


def score_email(summary_metadata, uuid):
    '''
    Calculate quality score for administrative contact
    '''
    score = 0
    if summary_metadata.loc[uuid, "has_adm_or_metadata_contact"]:
        score += 1
    if summary_metadata.loc[uuid, "has_adm_or_metadata_contact_email"]:
        score += 1
    return score


def score_geographic_coverage(summary_metadata, uuid):
    '''
    Calculate quality score for geographic coverage
    '''
    score = 0
    if summary_metadata.loc[uuid, "has_bounding_box"]:
        score += 1
    if summary_metadata.loc[uuid, "has_geographic_descrition"]:
        score += 1
    return score


def score_time_coverage(summary_metadata, uuid):
    '''
    Calculate quality score for time coverage
    '''
    score = 0
    if summary_metadata.loc[uuid, "number_of_dates"] > 0:
        score += 1
    return score


def score_method(summary_metadata, uuid):
    '''
    Calculate quality score for time coverage
    '''
    score = 0
    if summary_metadata.loc[uuid, "has_qualityControl"] or summary_metadata.loc[uuid, "has_studyExtent"] or summary_metadata.loc[uuid, "has_sampling"]:
        score += 1
    if summary_metadata.loc[uuid, "has_qualityControl"] and summary_metadata.loc[uuid, "has_studyExtent"] and summary_metadata.loc[uuid, "has_sampling"]:
        score += 1
    return score


def make_individual_plot(ax, uuid, summary_metadata, score, base_radius, size, label = False):
    '''
    Plot piechart for metadata score for one dataset
    '''
    my_labels = []
    bars = []
    circle_colors = []

    for category in score:
        my_labels.append(score[category]["label"])
        bars.append(score[category]["length"])
        circle_colors.append(score[category]["score"][summary_metadata.loc[uuid, category]])
    if label:
        ax.pie(bars, radius=base_radius, colors=circle_colors,
               wedgeprops=dict(width=size, edgecolor='w'), labels=my_labels)
    else:
        ax.pie(bars, radius=base_radius, colors=circle_colors,
               wedgeprops=dict(width=size, edgecolor='w'))
    ax.set(aspect="equal")
    return ax


def plot_entire_dataset(ax, summary_metadata, score, size=0.05):
    '''
    Plot piechart for metadata score for an entire pandas dataset
    '''
    fig, ax = plt.subplots()
    base_radius = summary_metadata.shape[0]*size

    for uuid in summary_metadata.index.tolist():
        if uuid == summary_metadata.index.tolist()[0]:
            ax = make_individual_plot(ax, uuid, summary_metadata, score, base_radius, size, True)
        else:
            base_radius = base_radius-size
            ax = make_individual_plot(ax, uuid, summary_metadata, score, base_radius, size)
    plt.show()

