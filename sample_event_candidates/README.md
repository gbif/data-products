# Identifiying datasets of type (Sample Event)

The mission is to enable users to identify datasets most relevant to their purpose. Tagging or categorizing the GBIF datasets will serve as a launchpad for our effort to make this kind of filtering possible. Example: "Give me all records from sediment-corer type samples"
Initially all datasets in GBIF should be parsed by using a range of keywords that signify a sampling event dataset.
These can be ['plot', 'transect', 'trap', 'trawl'] (of course there are many others) and I used these for the prototyping.

The repository for these terms is this:
https://docs.google.com/spreadsheets/d/16lEFzwLVBfjONXGflnLpWre_kDnhrRKdU9hPnmqr_M4/edit#gid=2049077323

|               |                    |
| ------------- |:------------------|
|![alt text](https://github.com/gbif/data-products/blob/master/sample_event_candidates/SampEvent_drawexpress.png)      | The first step is to assemble *sampling protocol terms* which is a large subject unto itself.<br/>We would want members of the community with knowledge in this area to contribute to the Sampling Event vocabulary.<br/>Once there is a pool of terms such as the list above would be part of, then we can throw them at GBIF ElasticSearch : `http://registry-search.gbif.org:9200/dataset/_search/` (only works inside GBIF firewall) |
|               |                     |



