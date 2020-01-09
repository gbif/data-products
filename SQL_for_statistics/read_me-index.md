## These SQL queries produce the yearly/monthly numbers that publishers most often demand. This also covers what goes into the Monthly Statistics ##

Unless stated *otherwise* all SQL declarations are for the Postgres registry database and use standard Postgres SQL.

* **user download stats SQL** (Registry Postgres)
  * User downloads (number of downloaded records) from a publishing country by publishing organization and by dataset:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/Downloaded_records_by_country_publisher_and_dataset.md
  * User downloads for one publisher the download events, sum of downloaded records _for each dataset_ that users downloaded between specific dates.
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/Publisher_download_stats_by_dataset
  * **Node Engagement** Number of datasets that a node is hosting through its publishing organizations:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/Node_engagement-count_of_hosted_datasets
  * Node download events, sum of downloaded records that users downloaded between specific dates for **one specific node**. If more nodes should be included use the IN statement in the WHERE clause.
  * The sum of records that users downloaded by month between specific dates _index wide_:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/total_records_total_events_and_total_users_downloaded_by_month
    
* **filter based user download stats SQL**
  * When searching inside the occurrence_download table's filter column, you will be dealing with JSON data. Postgres has not been well equipped to deal with JSON style data. For Postgres 11 which GBIF is using (tested 09-01-2020) the SQL posted in this repo will work.
  * Here is a sample of the flavor:
    *     SELECT t1.fil FROM
          (SELECT filter::json as fil FROM occurrence_download limit 1000)t1, json_array_elements(t1.fil->'predicates') AS pred
          WHERE pred->>'key' = 'COUNTRY'
   * You are selecting via a function in the subquery. Postgres doesn't natively recognize JSON which is why it must be cast as such ( ::json ). The json_array_elements() function turns each download filter into a 'table' or a _set_. The "->>" is one type of operator you can use to pick at the data. [JSON Functions and Operators](https://www.postgresql.org/docs/12/functions-json.html) 
   * User download filter statistics based on country georeference:
     * []https://github.com/gbif/data-products/blob/master/SQL_for_statistics/user_download_filer-COUNTRY_georeference-DOWNLOAD-EVENTS.md
  
* **Country publishing (HIVE DB)**
  * This gives the number of records shared by _publisher country_ and has _End-of-year_ SQL as well:
    * https://github.com/gbif/data-products/blob/master/SQL_for_statistics/SQL_for_Publishing-stats_by_publisher-country_HIVE
