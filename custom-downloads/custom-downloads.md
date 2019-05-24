# Custom Downloads On GBIF 

This is how you make a custom download for users wanting large or special files. 

## Step 1. HUE or HIVE part

Should be run in HUE or using HIVE command line. 

http://c5hue.gbif.org:8888/hue/editor?

Run this in the HUE editor to create a table. 

You will need a database with your name in place of `jwaller`.  You can create a datbase in HUE using the `+`. 

First go to the prod_g (or latest occurrence database). 

Create a table using. 

```
CREATE EXTERNAL TABLE jwaller.delimiter_csv (
  gbifId INT,
  v_scientificName STRING  
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '/user/jwaller/delimiter.csv'
```

Run in HUE your custom hive query. Make sure the names in the table you created above match the names you create in you custom query. 

```
INSERT OVERWRITE TABLE jwaller.delimiter_csv
SELECT 
  gbifId, 
  v_scientificName
FROM prod_g.occurrence_hdfs
LIMIT 100
```

## Step 2. 

Now we will copy the file into the production server in order to share the file with others. 

1. Log onto C5. `ssh jwaller@c5gateway-vh.gbif.org`
2. 
2. You can also make `mkdir jwaller`




```

hdfs dfs -getmerge /user/mgrosjean/oldName.csv newName.tsv

```
