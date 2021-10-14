
Make excel file for dormant publishers campaign
===============================================

The code in _make_excel_for_dormant_production.py_ is there to build the foundational spreadsheet used for running the 'Dormant Publishers campign'. The output excel file will go into the 365 Power Automate workflow for mass emailing to the publishers identified in the spread sheet. The reason we don't use the regular office mail-merge is that this does not allow grouping of several contacts into one conversation.

Since the code relies on the content of the GBIF API call: https://api.gbif.org/v1/organization/nonPublishing?limit=500
the only parameter that has to be set in the script is the directory and name of the output file:
>final_df.to_excel('dormant_2021_10-08_a.xlsx', index=False)

The only services the script depends on apart from the API call above are these two:  
https://api.gbif.org/v1/node/  
https://api.gbif.org/v1/organization/{}/hostedDataset


There is also a bit of out-commented code that can turn the final data frame into a pickle object for further processing by other Python scripts.
