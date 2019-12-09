## These SQL queries produce the yearly/monthly numbers that publishers most often demand. This also covers what goes into the Monthly Statistics ##

Unless stated *otherwise* all SQL declarations are for the Postgres registry database and use standard Postgres SQL.

* user download SQL (Registry Postgres)
  * User downloads from a publishing country by publishing organization and by dataset:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/country_records_user_download.md
  * User downloads for one publisher the download events, sum of downloaded records _for each dataset_ that users downloaded between specific dates.
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/Publisher_download_stats_by_dataset
  * Number of datasets that a node is hosting through its publishing organizations:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/Node_engagement-count_of_hosted_datasets
  * The sum of records that users downloaded by month between specific dates _index wide_:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/total_records_total_events_and_total_users_downloaded_by_month
  * Node download events, sum of downloaded records that users downloaded between specific dates for **one specific node**. If more nodes should be included use the IN statement in the WHERE clause.
  
* Country publishing (HIVE DB)
  * This gives the number of records shared by _publisher country_:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/SQL_for_Publishing-stats_by_publisher-country_HIVE
