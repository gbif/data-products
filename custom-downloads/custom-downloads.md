# Custom Downloads On GBIF 

This is how you make a custom download for users wanting large or special files. 

## Step 1. HUE or HIVE part

Should be run in HUE or using HIVE command line. You need permission to access these places. 

http://c5hue.gbif.org:8888/hue/editor?

Run this in the HUE editor to create a table. 

You will need a database with your name in place of `jwaller`.  You can create a datbase in HUE using the `+`. 

First go to the prod_g database (or latest occurrence hdfs database). 

Create a table using: 

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
FROM prod_g.occurrence_hdfs
LIMIT 100
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




