import json
import time
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_metadata_from_API(sample_datasets=None, exclude=None):
    '''
    Get the infor we want to monitor and display it
    '''
    fields_of_interest = ["type",
                          "title_len",
                          "description_len",
                          "language_metadata",
                          "contact_count",
                          "contact_type",
                          "contact_with_valid_email_count",
                          "taxonomicCoverages_description_len",
                          "taxonomicCoverages_scientificName_count",
                          "taxonomicCoverages_rank",
                          "geographicCoverages_description_len",
                          "geographicCoverages_boundaries_count",
                          "temporalCoverages_type",
                          "temporalCoverages_count",
                          "keywords",
                          "project_title_len",
                          "project_indetifier",
                          "samplingDescription_total_len",
                          "samplingDescription_field_filled",
                          "additionalInfo_len"]
    summary_metadata = pd.DataFrame(columns=fields_of_interest)
    if sample_datasets is not None:

        for uuid in sample_datasets:
            response = requests.get("http://api.gbif.org/v1/dataset/"+uuid)
            response = response.json()
            summary_metadata = update_dataframe(summary_metadata, uuid, response)
            time.sleep(1)
    else:
        offset = 0
        step = 300
        limit = offset + step
        end_of_records = False
        while not end_of_records:
            param = {
                "offset": offset,
                "limit": limit
            }
            response = requests.get("http://api.gbif.org/v1/dataset", param)
            response = response.json()
            for dataset in response["results"]:
                if exclude is not None:
                    if dataset["publishingOrganizationKey"] not in exclude:
                        summary_metadata = update_dataframe(summary_metadata, dataset["key"], dataset)
                else:
                    summary_metadata = update_dataframe(summary_metadata, dataset["key"], dataset)
            time.sleep(1)
            offset += step
            end_of_records = response["endOfRecords"]

    return summary_metadata


def update_dataframe(summary_metadata, uuid, response):
    '''
    Update all columns dataset for a given row
    '''

    # GLOBAL
    summary_metadata = update_dataframe_general_metadata(summary_metadata, uuid, response)

    # CONTACTS
    summary_metadata = update_dataframe_contact_metadata(summary_metadata, uuid, response)

    # TAXONOMY
    summary_metadata = update_dataframe_taxonomy_metadata(summary_metadata, uuid, response)

    # GEOGRAPHY
    summary_metadata = update_dataframe_geography_metadata(summary_metadata, uuid, response)

    # TIME
    summary_metadata = update_dataframe_time_metadata(summary_metadata, uuid, response)

    # KEYWORDS
    summary_metadata = update_dataframe_keyword_metadata(summary_metadata, uuid, response)

    # PROJECT
    summary_metadata = update_dataframe_project_metadata(summary_metadata, uuid, response)

    # METHOD
    summary_metadata = update_dataframe_method_metadata(summary_metadata, uuid, response)

    # ADDITIONAL INFO
    summary_metadata = update_dataframe_additionnal_info_metadata(summary_metadata, uuid, response)
    return summary_metadata


def update_dataframe_general_metadata(summary_metadata, uuid, response):
    '''
    Update general metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "type"] = response["type"]
    if "title" in response:
        summary_metadata.at[uuid, "title_len"] = len(response["title"])
    else:
        summary_metadata.at[uuid, "title_len"] = 0.0
    if "description" in response:
        summary_metadata.at[uuid, "description_len"] = len(response["description"])
    else:
        summary_metadata.at[uuid, "description_len"] = 0.0
    if "language" in response:
        summary_metadata.at[uuid, "language_metadata"] = response["language"]
    return summary_metadata


def update_dataframe_contact_metadata(summary_metadata, uuid, response):
    '''
    Update contact metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "contact_count"] = 0.0
    summary_metadata.at[uuid, "contact_type"] = []
    summary_metadata.at[uuid, "contact_with_valid_email_count"] = 0.0
    if "contacts" in response:
        for ind in response["contacts"]:
            summary_metadata.at[uuid, "contact_count"] += 1
            if "type" in ind:
                summary_metadata.at[uuid, "contact_type"].append(ind["type"])
            if "email" in ind:
                summary_metadata.at[uuid, "contact_with_valid_email_count"] += len(ind["email"])
    return summary_metadata


def update_dataframe_taxonomy_metadata(summary_metadata, uuid, response):
    '''
    Update taxonomy metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "taxonomicCoverages_description_len"] = 0.0
    summary_metadata.at[uuid, "taxonomicCoverages_scientificName_count"] = 0.0
    summary_metadata.at[uuid, "taxonomicCoverages_rank"] = []
    if "taxonomicCoverages" in response:
        for tax in response["taxonomicCoverages"]:
            if "description" in tax:
                summary_metadata.at[uuid, "taxonomicCoverages_description_len"] += len(tax["description"])
            if "coverages" in tax:
                for coverage in tax["coverages"]:
                    summary_metadata.at[uuid, "taxonomicCoverages_scientificName_count"] += 1
                    if "rank" in coverage:
                        if "interpreted" in coverage["rank"]:
                            summary_metadata.at[uuid, "taxonomicCoverages_rank"].append(coverage["rank"]["interpreted"])
    return summary_metadata


def update_dataframe_geography_metadata(summary_metadata, uuid, response):
    '''
    Update geography metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "geographicCoverages_boundaries_count"] = 0.0
    summary_metadata.at[uuid, "geographicCoverages_description_len"] = 0.0
    if "geographicCoverages" in response:
        for geo in response["geographicCoverages"]:
            if "description" in geo:
                summary_metadata.at[uuid, "geographicCoverages_description_len"] += len(geo["description"])
            if "boundingBox" in geo:
                boundaries_number = len(geo["boundingBox"].keys())
                if 'globalCoverage' in geo["boundingBox"]:
                    boundaries_number = boundaries_number - 1
                summary_metadata.at[uuid, "geographicCoverages_boundaries_count"] += boundaries_number
    return summary_metadata


def update_dataframe_time_metadata(summary_metadata, uuid, response):
    '''
    Update time metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "temporalCoverages_count"] = 0.0
    if "temporalCoverages":
        for time_coverage in response["temporalCoverages"]:
            type_temporal_coverage = 0.0
            if "@type" in time_coverage:
                summary_metadata.at[uuid, "temporalCoverages_type"] = time_coverage["@type"]
                type_temporal_coverage += 1
            if "type" in time_coverage:
                type_temporal_coverage += 1
            summary_metadata.at[uuid, "temporalCoverages_count"] += (len(time_coverage)-type_temporal_coverage)
    return summary_metadata


def update_dataframe_keyword_metadata(summary_metadata, uuid, response):
    '''
    Update keyword metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "keywords"] = []
    if "keywordCollections" in response:
        for keyword in response["keywordCollections"]:
            if "keywords" in keyword:
                summary_metadata.at[uuid, "keywords"] += keyword["keywords"]
    return summary_metadata


def update_dataframe_project_metadata(summary_metadata, uuid, response):
    '''
    Update project metadata columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "project_title_len"] = 0.0
    if "project" in response:
        if "title" in response["project"]:
            summary_metadata.at[uuid, "project_title_len"] += len(response["project"]["title"])
        if "identifier" in response["project"]:
            summary_metadata.at[uuid, "project_indetifier"] = response["project"]["identifier"]
    return summary_metadata


def update_dataframe_method_metadata(summary_metadata, uuid, response):
    '''
    Update project method columns of a dataset for a given row
    '''
    summary_metadata.at[uuid, "samplingDescription_total_len"] = 0.0
    summary_metadata.at[uuid, "samplingDescription_field_filled"] = []
    if "samplingDescription" in response.keys():
        for para_title in response["samplingDescription"]:
            summary_metadata.at[uuid, "samplingDescription_total_len"] += len(response["samplingDescription"][para_title])
            summary_metadata.at[uuid, "samplingDescription_field_filled"].append(para_title)
    return summary_metadata


def update_dataframe_additionnal_info_metadata(summary_metadata, uuid, response):
    '''
    Update project additional info columns of a dataset for a given row
    '''
    if "additionalInfo" in response:
        summary_metadata.at[uuid, "additionalInfo_len"] = len(response["additionalInfo"])
    else:
        summary_metadata.at[uuid, "additionalInfo_len"] = 0.0
    return summary_metadata

def count_categories(my_summary, variable_of_interest, label_for_zero_count):
    '''
    Counts items in list in a given column
    '''
    all_type = pd.Series(my_summary[variable_of_interest].sum()).value_counts()
    my_type = all_type.append(pd.Series(len([my_summary[my_summary[variable_of_interest].apply(len) == 0]]),
                                        index=[label_for_zero_count]))
    return my_type


def plot_general_metadata(my_summary, example_summary, main_color, example_color, list_language_color):
    '''
    3 parts plot for title, description and language
    '''
    plt.close('all')
    plt.figure(figsize=(12, 7))
    ax1, ax2, ax3 = plt.subplot(221), plt.subplot(223), plt.subplot(222)

    # TITLE
    ax1.hist(my_summary.title_len.tolist(), bins=20, color=main_color)
    ax1.set_xlabel("Number of characters in title")
    ax1.set_ylabel("Frequency")

    # DESCRIPTION
    ax2.hist(my_summary.description_len.tolist(), bins=20, color=main_color)
    ax2.set_xlabel("Number of characters in decription")
    ax2.set_ylabel("Frequency")

    for line in example_summary.title_len.tolist():
        ax1.axvline(line, color=example_color, linestyle='--')
        ax2.axvline(line, color=example_color, linestyle='--')

    # LANGUAGES
    languages = my_summary.language_metadata.value_counts()
    ax3.pie(languages.tolist(), labels=languages.index, autopct='%1.1f%%',
            colors=list_language_color[0:len(languages.index)])
    ax3.set_title("Languages")
    plt.axis('equal')
    plt.tight_layout()


def plot_contact_metadata(my_summary,
                          main_color,
                          example_summary=None,
                          example_color='#bcc2c6',
                          alpha_example=0.6):
    '''
    3 part plot for contact points, emails and contact type
    '''
    contact_type = count_categories(my_summary, 'contact_type', 'no contact type')

    plt.close('all')
    plt.figure(figsize=(12, 7))
    ax1, ax2, ax3 = plt.subplot(221), plt.subplot(223), plt.subplot(122)

    # CONTACT POINTS
    ax1.hist(my_summary.contact_count.tolist(), bins=20, color=main_color)
    ax1.set_xlabel("Number of contact points")
    ax1.set_ylabel("Frequency")

    # EMAILS
    ax2.hist(my_summary.contact_with_valid_email_count.tolist(), bins=20, color=main_color)
    ax2.set_xlabel("Number of contact points with email")
    ax2.set_ylabel("Frequency")

    # CONTACT TYPE
    ax3.barh(y=np.arange(contact_type.size), width=contact_type.tolist(), color=main_color)
    plt.sca(ax3)
    plt.yticks(np.arange(contact_type.size), contact_type.index.tolist())
    ax3.set_title("Frequency of contact types")
    ax3.set_xlabel("Frequency")

    # ADD EXAMPLE
    if example_summary is not None:
        examples = count_categories(example_summary, 'contact_type', 'no contact type')
        ax3.barh(y=np.arange(examples.size), width=examples.tolist(), color=example_color, alpha=alpha_example)
        for index, line in example_summary.iterrows():
            ax1.axvline(line["contact_count"], color=example_color, linestyle='--')
            ax2.axvline(line["contact_with_valid_email_count"], color=example_color, linestyle='--')
    plt.tight_layout()


def plot_taxon_metadata(my_summary,
                        main_color,
                        alpha_one_bar,
                        example_summary=None,
                        example_color='#bcc2c6',
                        alpha_example=0.6):
    '''
    3 parts plot for description, scientific names and taxon ranks
    '''
    ranks = count_categories(my_summary, 'taxonomicCoverages_rank', 'NO TAXON')
    plt.close('all')
    plt.figure(figsize=(12, 7))
    ax1, ax2, ax3 = plt.subplot(221), plt.subplot(223), plt.subplot(122)

    # DESCRIPTION
    ax1.hist(my_summary.taxonomicCoverages_description_len.tolist(), bins=20, color=main_color)
    ax1.set_xlabel("Number of characters in taxonomic coverage description")
    ax1.set_ylabel("Frequency")

    # SCIENTIFIC NAMES
    ax2.hist(my_summary.taxonomicCoverages_scientificName_count.tolist(), bins=20, color=main_color)
    ax2.set_xlabel("Number of scientific names entered in taxonomic coverage")
    ax2.set_ylabel("Frequency")

    # TAXON RANKS
    alpha = 1
    if ranks.size == 1:
        alpha = alpha_one_bar
    ax3.barh(y=np.arange(ranks.size), width=ranks.tolist(), color=main_color, alpha=alpha)
    plt.sca(ax3)
    plt.yticks(np.arange(ranks.size), ranks.index.tolist())
    ax3.set_title("Frequency of taxon rank used in taxonomic coverage")
    ax3.set_xlabel("Frequency")

    # ADD EXAMPLE
    if example_summary is not None:
        examples = count_categories(example_summary, 'taxonomicCoverages_rank', 'NO TAXON')
        ax3.barh(y=np.arange(examples.size), width=examples.tolist(), color=example_color, alpha=alpha_example)
        for index, line in example_summary.iterrows():
            ax1.axvline(line["taxonomicCoverages_description_len"], color=example_color, linestyle='--')
            ax2.axvline(line["taxonomicCoverages_scientificName_count"], color=example_color, linestyle='--')
    plt.tight_layout()


def plot_geographic_metadata(my_summary,
                             main_color,
                             example_summary=None,
                             example_color='#bcc2c6'):
    '''
    2 parts for decsription and bounding box
    '''
    plt.close('all')
    plt.figure(figsize=(13, 8))
    ax1, ax2 = plt.subplot(221), plt.subplot(222)

    # DESCRIPTION
    ax1.hist(my_summary.geographicCoverages_description_len.tolist(), bins=20, color=main_color)
    ax1.set_xlabel("Number of characters in geographic coverage description")
    ax1.set_ylabel("Frequency")

    # BOUNDARIES
    ax2.hist(my_summary.geographicCoverages_boundaries_count.tolist(), bins=20, color=main_color)
    ax2.set_xlabel("Number of boundaries in geographic coverage")
    ax2.set_ylabel("Frequency")

    # ADD EXAMPLE
    if example_summary is not None:
        for index, line in example_summary.iterrows():
            ax1.axvline(line["geographicCoverages_description_len"], color=example_color, linestyle='--')
            ax2.axvline(line["geographicCoverages_boundaries_count"], color=example_color, linestyle='--')
    plt.tight_layout()


def plot_time_metadata(my_summary,
                       main_color,
                       list_type_color,
                       example_summary=None,
                       example_color='#bcc2c6'):
    '''
    2 parts plot for type of time entry and number of dates
    '''
    type_coverage = my_summary.temporalCoverages_type.value_counts()
    plt.close('all')
    plt.figure(figsize=(13, 8))
    ax1, ax2 = plt.subplot(221), plt.subplot(222)

    # TYPE
    ax1.pie(type_coverage.tolist(), labels=type_coverage.index, autopct='%1.1f%%', colors=list_type_color)
    ax1.set_title("Types of time coverage")
    ax1.axis('equal')
    # DATES
    ax2.hist(my_summary.temporalCoverages_count.tolist(), bins=20, color=main_color)
    ax2.set_xlabel("Number of dates in temporal coverage")
    ax2.set_ylabel("Frequency")
    # ADD EXAMPLE
    if example_summary is not None:
        for index, line in example_summary.iterrows():
            ax2.axvline(line["temporalCoverages_count"], color=example_color, linestyle='--')
    plt.tight_layout()


def plot_keyword_metadata(my_summary,
                          main_color,
                          number_kw=10,
                          example_summary=None,
                          example_color='#bcc2c6'):
    '''
    2 parts for number of keywords and top X keywords
    '''
    top_kw = pd.Series([item for sublist in my_summary.keywords.tolist() for item in sublist]).value_counts()[0:number_kw]

    plt.close('all')
    plt.figure(figsize=(13, 8))
    ax1, ax2 = plt.subplot(221), plt.subplot(222)

    # AMOUNT
    ax1.hist(my_summary.keywords.apply(len).tolist(), bins=20, color=main_color)
    ax1.set_xlabel("Number of keywords by dataset")
    ax1.set_ylabel("Frequency")

    # TOP X
    plt.setp(plt.gca(), frame_on=False, xticks=(), yticks=())
    ax2.text(0.35, 0.5, "\n".join(top_kw.index.tolist()),
             verticalalignment='center',
             transform=ax2.transAxes,
             fontsize=13)
    ax2.set_title("Top "+str(number_kw)+" keywords")

    # ADD EXAMPLE
    if example_summary is not None:
        for line in example_summary.keywords.apply(len).tolist():
            ax1.axvline(line, color=example_color, linestyle='--')
    plt.tight_layout()


def plot_medthod_metadata(my_summary,
                          main_color,
                          alpha_one_bar,
                          example_summary=None,
                          example_color='#bcc2c6',
                          alpha_example=0.6):
    '''
    2 parts plot for description and type of paragrah filled
    '''
    methods = count_categories(my_summary, 'samplingDescription_field_filled', 'NO paragraph')

    plt.close('all')
    plt.figure(figsize=(13, 8))
    ax1, ax2 = plt.subplot(221), plt.subplot(222)

    # DESCRIPTION
    ax1.hist(my_summary.samplingDescription_total_len.tolist(), bins=20, color=main_color)
    ax1.set_xlabel("Number of character in Method/Sampling description")
    ax1.set_ylabel("Frequency")

    # PARAGRAPH FILLED
    alpha = 1
    if methods.size == 1:
        alpha = alpha_one_bar
    ax2.barh(y=np.arange(methods.size), width= methods.tolist(), color=main_color, alpha=alpha)
    plt.sca(ax2)
    plt.yticks(np.arange(methods.size), methods.index.tolist())
    ax2.set_title("Frequency of fields filled in Method")
    ax2.set_xlabel("Frequency")
    plt.subplots_adjust(wspace=0.3)

    # ADD EXAMPLE
    if example_summary is not None:
        examples = count_categories(example_summary, 'samplingDescription_field_filled', 'NO paragraph')
        ax2.barh(y=np.arange(examples.size), width= examples.tolist(), color=example_color, alpha=alpha_example)
        for index, line in example_summary.iterrows():
            ax1.axvline(line["samplingDescription_total_len"], color=example_color, linestyle='--')
    plt.tight_layout()
    