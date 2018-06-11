# Data Products

This repository is for the Data Product team.

## Data Quality

### Metadata
In order to get quality metadata, we would like to identify:
* what we have
* what we are missing
* what can be improved

The metadata folder contains scripts and files generated using the [GBIF registry API](https://www.gbif.org/developer/registry) to retrieve and visualise information about about metadata's datasets.
The goal is to get an overview of the quality of the metadata.

To see the plots generated, you can check the ipython notebooks:
* [for the BID datasets](https://github.com/gbif/data-products/blob/master/metadata/visualise_metadata_BID_datasets.ipynb)
* [for all the datasets except PLAZIs](https://github.com/gbif/data-products/blob/master/metadata/visualise_metadata_all_datasets.ipynb) (these plots are not very informative as such, the outliers stretch the scale a lot, but the data these plots are made with are available [here](https://github.com/gbif/data-products/blob/master/metadata/summary_all_metadata_PLAZIexcluded_20180608.txt), you can use them if you do not with to rerun everything).

NB: you need to rerun them if you wish to have more recent plots.

Recommendations to improve metadata quality will be written in this repository's wiki.
