
Make excel file for dormant publishers campaign
===============================================

The code in make_excel_for_dormant_production.py is there to build the foundational spreadsheet using for running the 'Dormant Publishers campign'. The output excel file will go into the 365 Power Automate workflow for mass emailing to the publishers identified in the spread sheet. 
Since the code relies on the content of the GBIF API call: https://api.gbif.org/v1/organization/nonPublishing?limit=500
the only parameter that has to be set in the script is the directory and name of the output file:
>final_df.to_excel('dormant_2021_10-08_a.xlsx', index=False)

There is also a bit of out-commented code that can turn the final data frame into a pickle object for further processing by other Python scripts.
