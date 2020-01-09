# User download filter statistics based on country georeference

#### This SQL will get you the download events for a year based on the filter column in the _occurrence_download_ table. If the user selected for _country_ or used a _coordinate_, that download will be counted.

    SELECT t1.title, count(t1.fil) FROM (
    SELECT filter::json as fil, d.title as title, occurrence_download.created as crea FROM occurrence_download 
    JOIN dataset_occurrence_download dod ON occurrence_download.key = dod.download_key 
    JOIN dataset d ON dod.dataset_key = d.key
    WHERE is_json(filter) AND d.publishing_organization_key = '174c6da2-e002-42fe-9f56-2f9d670240f4' AND occurrence_download.status IN ('SUCCEEDED', 'FILE_ERASED') AND date(occurrence_download.created) BETWEEN '2019-01-01' AND '2019-12-31'
    )t1, json_array_elements(t1.fil->'predicates') AS pred
    --WHERE pred->>'key' = 'COUNTRY' 
    WHERE pred->>'key' = 'HAS_COORDINATE' 
    GROUP BY 1 ORDER BY 1

You can switch between 'COUNTRY' and 'HAS_COORDINATE' by moving the out comment.
