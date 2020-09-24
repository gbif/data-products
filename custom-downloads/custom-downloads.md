# Custom Downloads On GBIF 

This is how you make a custom download for users wanting large or special files. 

## Step 1. HUE or HIVE part

Should be run in HUE or using HIVE command line. You need permission to access these places. 

1. go to http://c5hue.gbif.org:8888/hue/editor?
2. You will need a database with your name in place of `jwaller`.  You can create a datbase in HUE using the `+`. 
3. Next go to the `prod_h` database (or latest occurrence hdfs database). 

Run this in the HUE editor to create a table: 

```
CREATE EXTERNAL TABLE jwaller.delimiter_csv (
  gbifId INT,
  v_scientificName STRING  
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '/user/jwaller/delimiter.csv'
```

Now run in HUE your custom hive query. Make sure the names in the table you created above match the names you create in you custom query. 

```
INSERT OVERWRITE TABLE jwaller.delimiter_csv
SELECT 
  gbifId, 
  v_scientificName
FROM prod_h.occurrence_pipeline_hdfs
LIMIT 100
```

**Note on converting dates from BIGINT to ISO format:**

We are going to use our download occurrence library. First let's check what is the latest available version. There are two possible solutions for that.
* Use the follwing command: `hdfs dfs -ls /occurrence-download-workflows-prod/lib`
* Or check one of these two links (one will work while the other will return an error message, we can't know which one will work):
  * http://c5hdfs1.gbif.org:50070/explorer.html#/occurrence-download-workflows-prod/lib
  * http://c5hdfs2.gbif.org:50070/explorer.html#/occurrence-download-workflows-prod/lib
  
Then in Hive:
```
ADD JAR hdfs://ha-nn/occurrence-download-workflows-prod/lib/occurrence-download-0.122.jar; -- check version first
CREATE TEMPORARY FUNCTION toLocalISO8601 AS 'org.gbif.occurrence.hive.udf.ToLocalISO8601UDF';

SELECT toLocalISO8601(eventdate) AS eventdate FROM ...
```
There is also a function to join the issues, media type and recordedById arrays with semicolons:
```
CREATE TEMPORARY FUNCTION joinArray AS 'brickhouse.udf.collect.JoinArrayUDF';

SELECT if(mediatype IS NULL,'',joinArray(mediatype,'\\;')) AS mediatype, ...
```

## Step 2. Copying the table to production server

Now we will copy the file into the production server in order to share the file with others. 

1. Log onto C5. `ssh jwaller@c5gateway-vh.gbif.org`
2. Go to `cd /mnt/auto/misc/download.gbif.org/custom_download`
3. You can now optionally make a personal directory `mkdir jwaller`

Finally run this command to copy the file into the `custom_download` folder. 

```
hdfs dfs -getmerge /user/jwaller/delimiter.csv customDownloadTest.tsv
```

You should now be able to see your custom download at this webpage. 
http://download.gbif.org/custom_download/

You can now simply share the link with the user and they should be able to download the file. The link we created in the example should now be at: 
http://download.gbif.org/custom_download/jwaller/customDownloadTest.tsv




