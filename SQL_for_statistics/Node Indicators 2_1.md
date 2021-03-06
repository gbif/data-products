## SQL for 2.1 Hosting other publishers datasets. A measure of the willingness of the node network to host on behalf of other publishers. 

```
SELECT t2.node, t2.publisher, t2.publisher_key, sum(t2.count) FROM (
SELECT  t1.* FROM (
SELECT node.title AS node, o.title AS publisher, o.KEY AS publisher_key, d.installation_key AS ikey , count(*) FROM organization o
JOIN installation i ON i.organization_key = o.key
JOIN dataset d ON i.key = d.installation_key
JOIN node ON node.key = o.endorsing_node_key
WHERE d.deleted IS NULL 
AND o.key != d.publishing_organization_key AND node."type" = 'COUNTRY' 
AND date(o.created) < '2021-01-01' 
GROUP BY node, publisher, ikey, o.key
)t1
RIGHT JOIN node ON t1.node = node.title
WHERE node.deleted IS NULL AND t1.node IS NOT NULL
)t2 
GROUP BY 1,2,3 ORDER BY 1;
```



Please notice that only type country nodes are considered.


**Sanity check:**
Looking at the SQL query result there is this data point:

|node|publisher   |publisher_key   |count   |
|---|---|---|---|
|Burkina Faso   |FasoBIF           |9764f31c-f399-4912-97fd-01ebf8b8141c   |2   |


Look up the publisher key in the api : https://api.gbif.org/v1/dataset/search?hostingOrg=9764f31c-f399-4912-97fd-01ebf8b8141c
We see that the count is 2, The "hostingOrganizationKey": "9764f31c-f399-4912-97fd-01ebf8b8141c", and      "hostingOrganizationTitle" is "FasoBIF" in both cases, yet the publishing organizations are CNRST/INERA and SP/CONEDD-DCIME respectively. This checks out because the hosting org is not the publisher.
Another data point to look at is:
|node|publisher   |publisher_key   |count   |
|---|---|---|---|
|Ghana Biodiversity Information Facility      |Ghana Biodiversity Information Facility (GhaBIF)           |4bc4943a-c94f-4bd4-9aa3-2a9cae94398a   |8   |



Look up: https://api.gbif.org/v1/dataset/search?hostingOrg=4bc4943a-c94f-4bd4-9aa3-2a9cae94398a
Here we see the count of 9 rather than 8. However one entry is GhaBIF hosting itself, so this also checks out. 
