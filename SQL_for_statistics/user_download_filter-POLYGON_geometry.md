# User download filter statistics based on polygon geometry

### This SQL will get you the download events for a year based on the filter column in the occurrence_download table. If the user selected for a _polygon_, that download will be counted.

    SELECT t1.title, count(t1.fil) FROM (
    SELECT filter::json as fil, d.title as title, occurrence_download.created as crea FROM occurrence_download 
    JOIN dataset_occurrence_download dod ON occurrence_download.key = dod.download_key 
    JOIN dataset d ON dod.dataset_key = d.key
    WHERE is_json(filter) AND d.publishing_organization_key = '6ea87510-0561-11d8-b851-b8a03c50a862' AND occurrence_download.status IN ('SUCCEEDED', 'FILE_ERASED') AND date(occurrence_download.created) BETWEEN '2018-01-01' AND '2018-12-31'
    )t1, json_array_elements(t1.fil->'predicates') AS pred
    WHERE pred->>'geometry' ~ 'POLYGON*'     
    GROUP BY 1 
    
The thing to notice here is the ~ operator because we are allowing for polygons (plural).    
