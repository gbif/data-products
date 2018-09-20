# Data Products

This repository is for the Data Product team.

## Data Quality

### Metadata
In order to get quality metadata, we would like to identify:
* what is there
* what is missing
* what can be improved

The metadata folder contains scripts and files generated using the [GBIF registry API](https://www.gbif.org/developer/registry) to retrieve and visualise information about about metadata's datasets.
The goal is to get an overview of the quality of the metadata.


To see the plots generated to visualise baseline metrics, you can check the ipython notebooks:
* [for some of the BID datasets](https://github.com/gbif/data-products/blob/master/metadata/baseline_metrics_metadata_BID_datasets.ipynb)
* [for a sample of all the datasets except PLAZIs, GEOTAGs or PANGEAs](https://github.com/gbif/data-products/blob/master/metadata/baseline_metrics_metadata_all_dataset_NO_plazi_geotag_pangea.ipynb)

NB: you need to rerun them if you wish to have more recent plots.

The metrics chosen to represent metadata quality are detailed in the repository [Metadata wiki](https://github.com/gbif/data-products/wiki/Metadata).
