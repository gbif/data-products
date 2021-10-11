GBIF_API_caller
===============

This Python class **SearchAPI** can make API calls from a list of values and will parse the JSON response which is then outputted to a **flat text file** (tab separated).
It presupposes that the call is made to the GBIF Portal API http://www.gbif.org/developer/summary
Only the Species API and the Occurrence API have been tested.

Here is a usage example:

>my_api = SearchAPI(
>'http://api.gbif.org/v1/species/match?name=', 
>'D:/test/species.txt', 
>'D:/test/GBIFinterpreted_names.txt'
>)

>my_api.take_parameters("usageKey", "scientificName", "canonicalName", "rank")

The first argument is the search url, in this case it must contain everything except the variable that comes from text file in the second argument. The third argument is the output file.

See the exeSearch file for more examples.


Make excel file for dormant publishers campaign
===============================================

The code in make_excel_for_dormant_production.py is there to build the foundational spreadsheet using for running the 'Dormant Publishers campign'. The output excel file will go into the 365 Power Automate workflow for mass emailing to the publishers identified in the spread sheet. 
Since the code relies on the content of the GBIF API call: https://api.gbif.org/v1/organization/nonPublishing?limit=500
the only parameter that has to be set in the script is the directory and name of the output file:
>final_df.to_excel('dormant_2021_10-08_a.xlsx', index=False)

There is also a bit of out-commented code that can turn the final data frame into a pickle object for further processing by other Python scripts.
