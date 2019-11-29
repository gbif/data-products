This SQL produces a sum of the records downloaded from a publishing country by publishing organization and by dataset.
Excluded are deleted publishers and deleted datasets. Also excluded are downloads from @gbif.org addresses and where there is no filter i.e. full index downloads assuming most of these are mistakes.
    
    SELECT o.title, d.title,  sum(dod.number_records) FROM dataset d
    JOIN organization o ON o.key = d.publishing_organization_key 
    JOIN dataset_occurrence_download dod ON d.key = dod.dataset_key
    JOIN occurrence_download od ON od.key = dod.download_key
    WHERE o.country = 'AT' AND o.deleted IS NULL AND d.deleted IS NULL 
    AND date(od.created) BETWEEN '2018-01-01' AND '2018-12-31' 
    AND od.status = 'SUCCEEDED' AND od.notification_addresses NOT LIKE '%@gbif.org' AND od.filter IS NOT NULL
    GROUP BY 1, 2
    ORDER BY 1

    
