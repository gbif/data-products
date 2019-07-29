# coding: utf-8
import pandas as pd
import requests
import argparse


def main(input_file, ouptut_file, species_api="http://api.gbif.org/v1/species/match?verbose=true&name="):
    '''
    Species matching API
    This scripts aims to emulate the GBIF species matching tool
    on GBIF (https://www.gbif.org/tools/species-lookup).
    It takes and input file containing scientific names
    (under the column `scientificName`) and look up a match in
    the GBIF taxonomy.
    
    The aletrnative matches are also included in the output file (they
    are tagged in the `is_alternative`).
    
    The scripts uses the GBIF Species API (https://www.gbif.org/developer/species):
    ```
    http://api.gbif.org/v1/species/match?
    ```
    '''
    # Upload species list
    species_list = pd.read_csv(input_file)  # make sure that file is UTF-8
    
    matched_species = []
    # For each name
    for species in species_list.index:
        
        # Replace space by %20 for API request in names
        name = species_list.loc[species, "scientificName"].replace(" ", "%20")
        
        # Find a match for the name with the API
        match = requests.get(species_api+name)
        
        # If the response is ok
        if match.ok:
            
            # Process the response
            match_result = match.json()
            match_result["inputName"] = species_list.loc[species, "scientificName"]
            
            # If the response contains alternative matches, make one line per match
            if "alternatives" in match_result:
                match_result["has_alternatives"] = True
                for alt in match_result["alternatives"]:
                    alt["inputName"] = species_list.loc[species, "scientificName"]
                    alt["is_alternative"] = True
                    matched_species.append(alt)  # add alternative
                match_result.pop('alternatives')
                
            # Strore the result
            matched_species.append(match_result)

    result = pd.DataFrame(matched_species)

    # Store taxon keys as integers
    taxon_keys = ['acceptedUsageKey', 'usageKey', 'kingdomKey', 'phylumKey','classKey', 'orderKey', 'familyKey', 'genusKey', 'speciesKey']
    result[taxon_keys] = result[taxon_keys].fillna(0).astype(int)

    # Fill NAs with NULL
    result = result.fillna("NULL")
    # Save file
    result.to_csv(ouptut_file, index=False, sep="\t")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Takes input file and looks for match in the GBIF backbone taxonomy')
    parser.add_argument('--in', dest='input_file', type=str, required=True, help='File containing list of names to check')
    parser.add_argument('--out', dest='ouptut_file',type=str, required=True,  help="File to store the result of the query")

    args = parser.parse_args()
    # Launch main function
    main(args.input_file, args.ouptut_file)
