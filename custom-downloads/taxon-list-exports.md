# Long taxonkey list downloads/exports

Sometimes users want to download a lot of taxonkeys like **>40K in some cases**. This is not possible to do via the website or using curl or something like that. 

> Note this walk through is for internal use and a regular user will not be able to do this (although see [here](https://github.com/ropensci/rgbif/issues/362) if you still want to make a somewhat large taxonkey download yourself). 

If the taxonkey list is less than around 5K [see dicussion here](https://github.com/ropensci/rgbif/issues/362) then it is probably easier to do a download using a http GET request. It might also be possible to break up big downloads into ~5K-taxonkey chunks, but if even that is too many downloads, a taxonkey list custom download might be worth while or still requested. 
 
# Matching the names

Users will not always provide you with taxonkey lists. Often they will give you just a list of names. Therefore it is necessary to get taxon keys before moving forward. 

I have a included a command-line-tool written by Marie that will match `species-matching-gbif-api.py` names to the backbone.

1. Install python 3
2. `pip install pandas` `pip install requests` 
3. `python species-matching-gbif-api.py --in yourInputFile.txt --out output.txt` 

Where `input.txt` is the names given to you by the user separated by a space. With **scientificName** as the column name. 

Sample `input.txt` file: 

```
scientificName
Aaptos suberitoides 
Aaptos pernucleata 
Aaptos lobata 
Aaptos lithophaga 
Aaptos laxosuberites 
Aaptos duchassaingi 
Aaptos chromis 
Aaptos bergmanni 
Aaptos adriatica 
Aaptos aaptos 
Aartsenia candida
Abraliopsis hoylei pfefferi
```

I cleaned up the `output.txt` file using the following R code. 

```
library(dplyr)
library(tibble)

D = data.table::fread("C:/Users/ftw712/Desktop/non_fish_download/output.txt") %>% as_tibble()

good = D %>% 
select(usageKey,rank,canonicalName,inputName,matchType) %>%
filter(matchType == "EXACT") %>%
filter(rank == "SPECIES" | rank == "SUBSPECIES") %>% # only keep species if the user gave you species names.
unique() %>% 
select(interpreted_taxonkey=usageKey,interpreted_rank=rank,interpreted_name =canonicalName,your_original_name = inputName,name_match_quality=matchType)

readr::write_tsv(good,path="interpreted_names.tsv",col_names=FALSE)
```

# Making a long taxonkey-list exports 

In this example I will be using a list for a **non_fish_export**. The `taxonkeys.txt` file can be found [here](https://github.com/gbif/data-products/blob/master/custom-downloads/taxonkeylist.txt). I will be using **Spark** but probably this could just as easily be achieved using HIVE. 

`taxonkey.txt` sample:
```
2242217
2242221
2242221
2225726
7912255
2267949
2268007
2268011
7598638
4343190
4582637
4582637
2242412
2242415
2265679
2265681
```

1. Copy `taxonkeys.txt` onto `scp -r /cygdrive/c/Users/ftw712/Desktop/taxonkeys.txt jwaller@c4gateway-vh.gbif.org:/home/jwaller/`
2. Create your own person database if does not exist use `+` button in HUE. 
3. Log on to server `ssh jwaller@c4gateway-vh.gbif.org`
4. Start `spark2-shell` scala shell

Do the following inside a `spark2-shell` session: 
```
val sqlContext = new org.apache.spark.sql.SQLContext(sc);
```




Create empty table where we will load our `taxonkeys.txt` 
```
sqlContext.sql(s"CREATE TABLE jwaller.interpreted_nonfish_taxonkeys (nonfish_taxonkey INT)");
```
You will now be able to see this table **interpreted_nonfish_taxonkeys** if you run `sqlContext.sql("show tables from jwaller").show();`. You could also view it inside HUE if you click the refresh button. You can delete this table by using `sqlContext.sql(s"DROP TABLE IF EXISTS jwaller.interpreted_nonfish_taxonkeys");`

Now I will load data into the table. Make sure you started your `spark2-shell` session in the same directory that `taxonkeys.txt` is located. 
```
sqlContext.sql(s"LOAD DATA LOCAL INPATH './taxonkeys.txt' OVERWRITE INTO TABLE jwaller.interpreted_nonfish_taxonkeys");
```
The data is now loaded. You could look at the table inside HUE **jwaller.interpreted_nonfish_taxonkeys**. 

Next we will make the data available as a dataframe **nonfish** in spark. I added `.distinct()` onto the end of the command because we only want unique taxonkeys. Duplicate taxonkeys will join to make duplicate records later on. 

```
val nonfish = sqlContext.sql("SELECT * FROM jwaller.interpreted_nonfish_taxonkeys").distinct();
```

Since the occurrence table has a **>400 columns**, we need to define the columns that we **want to keep**. There is probably no clever way to do this **since we simply need to define what we want in a big long list**. I will plug this in later into a select expression. `sqlContext.sql("SELECT " + columnsToKeep + " FROM uat.occurrence_hdfs");`. Switch `uat` to the production table if needed. 

```
val columnsToKeep = "taxonkey,publishingorgkey,datasetkey,recordedby,eventdate,institutioncode,collectioncode,catalognumber,basisofrecord,identifiedby,dateidentified,v_scientificname,v_scientificnameauthorship,scientificname,kingdom,phylum,class,taxonrank,family,genus,countrycode,locality,county,continent,stateprovince,publishingcountry,decimallatitude,decimallongitude,v_coordinateprecision,hasgeospatialissues,depth,depthaccuracy,v_maximumdepthinmeters,v_minimumdepthinmeters,elevation,elevationaccuracy,v_maximumelevationinmeters,v_minimumelevationinmeters,gbifid,specieskey,taxonid";

val D = sqlContext.sql("SELECT " + columnsToKeep + " FROM uat.occurrence_hdfs");
```

Now we will **join** everything together to keep just the keys that we want. This should be a much smaller dataframe than the **occurrence_hdfs** table. You can check by using `mergedDf.count();`. Remember we defined **nonfish_taxonkey** at the beginning when we created the **interpreted_nonfish_taxonkeys** table.

```
val mergedDf = nonfish.join(D,D("taxonkey") === nonfish("nonfish_taxonkey"));
```

Now create a temporary table from the **mergedDf** dataframe. We need this table because we are going to copy the results from it into a new **external table** we are creating below. You can check whether **non_fish_temp** was created by using `sqlContext.sql("show tables from jwaller").show();`.

```
mergedDf.createOrReplaceTempView("non_fish_temp");
```

The next part will create a new table external table. This will create an empty **external** table called **non_fish** with the same column names as **mergedDf**. This eternal table will be accessbile to `hdfs dfs -getmerge`, which we will use later to combine the distributed file into a **single file**. 

```
val x = mergedDf.columns.toSeq.mkString(" STRING, ");
val hive_sql = "CREATE EXTERNAL TABLE jwaller.non_fish (" + x + " STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' STORED AS TEXTFILE LOCATION '/user/jwaller/non_fish.csv'";
sqlContext.sql(hive_sql);

sqlContext.sql("show tables from jwaller").show(); // check result
```

Now I take the data from the temporary table **non_fish_temp** and copy it into **non_fish**. 
```
sqlContext.sql(s"INSERT OVERWRITE TABLE jwaller.non_fish SELECT * FROM non_fish_temp");
sqlContext.sql("SELECT * FROM jwaller.non_fish").count(); // check result
```

**This is the end of the spark shell part**

# Final steps 

These steps are to be excuted inside a normal terminal shell but still on the remote server of course. 

1. Go to `cd /mnt/auto/misc/download.gbif.org/custom_download/jwaller/`
2. Run to combine the file `hdfs dfs -getmerge /user/jwaller/non_fish.csv non_fish_export.tsv`
3. Optionally clean up weird **\N** instead of null `sed -i 's#\\N##g' non_fish_export.tsv`
4. You can also add a **header** to the file like this. I am not sure if this will work for really large files.  
```
sed -i '1i nonfish_taxonkey\ttaxonkey\tpublishingorgkey\tdatasetkey\trecordedby\teventdate\tinstitutioncode\tcollectioncode\tcatalognumber\tbasisofrecord\tidentifiedby\tdateidentified\tv_scientificname\tv_scientificnameauthorship\tscientificname\tkingdom\tphylum\tclass\ttaxonrank\tfamily\tgenus\tcountrycode\tlocality\tcounty\tcontinent\tstateprovince\tpublishingcountry\tdecimallatitude\tdecimallongitude\tv_coordinateprecision\thasgeospatialissues\tdepth\tdepthaccuracy\tv_maximumdepthinmeters\tv_minimumdepthinmeters\televation\televationaccuracy\tv_maximumelevationinmeters\tv_minimumelevationinmeters\tgbifid\tspecieskey\ttaxonid' non_fish_export.tsv
```
5. Finally **zip** the file. `zip non_fish_export.zip non_fish_export.tsv`
6. You can also remove the unzipped version `rm non_fish_export.tsv`

The file should now be viewable here: http://download.gbif.org/custom_download/





