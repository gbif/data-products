# Long taxonkey list download

Sometimes users want to download a lot of taxonkeys like **>40K in some cases**. This is not possible to do over via the website or using curl or something like that. 

> Note this walk through is for internal use and a regular user will not be able to do this (although see [here](https://github.com/ropensci/rgbif/issues/362) if you still want to make a large taxonkey download yourself). 

If the taxonkey list is less than around 5K [see dicussion here](https://github.com/ropensci/rgbif/issues/362) then it is probably easier to do a download using a http GET request. It might also be possible to break up big downloads into 5K-taxonkey chunks, but if even that is too many downloads if the list is very long. A taxonkey list custom download might be worth while or still requested. 
 
# Making a long taxonkey-list downloads 

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
The data is now loaded. You could look at now inside HUE **jwaller.interpreted_nonfish_taxonkeys**. 

Next we will make the data available as a dataframe **nonfish** in spark. I added `.distinct()` onto the end of the file because we only want unique taxonkeys. I am pretty sure duplicate taxonkeys will join to make duplicate records later on. 

```
val nonfish = sqlContext.sql("SELECT * FROM jwaller.interpreted_nonfish_taxonkeys").distinct();
```

Since the occurrence table has a **>400 columns**, we need to define the columns that we **want to keep**. There is probably no clever way to do this since we simply need to define what we want in a big long list. I will plug this in later into a select expression. `sqlContext.sql("SELECT " + columnsToKeep + " FROM uat.occurrence_hdfs");`. Switch `uat` to the production table if needed. 

```
val columnsToKeep = "taxonkey,publishingorgkey,datasetkey,recordedby,eventdate,institutioncode,collectioncode,catalognumber,basisofrecord,identifiedby,dateidentified,v_scientificname,v_scientificnameauthorship,scientificname,kingdom,phylum,class,taxonrank,family,genus,countrycode,locality,county,continent,stateprovince,publishingcountry,decimallatitude,decimallongitude,v_coordinateprecision,hasgeospatialissues,depth,depthaccuracy,v_maximumdepthinmeters,v_minimumdepthinmeters,elevation,elevationaccuracy,v_maximumelevationinmeters,v_minimumelevationinmeters,gbifid,specieskey,taxonid,ext_multimedia";

val D = sqlContext.sql("SELECT " + columnsToKeep + " FROM uat.occurrence_hdfs");
```

Now we will **join** everything together to keep just the keys that we want. This should be a much smaller dataframe. You can check by using `mergedDf.count();`. Remember we defined **nonfish_taxonkey** at the beginning when we created the **interpreted_nonfish_taxonkeys** table.

```
val mergedDf = nonfish.join(D,D("taxonkey") === nonfish("nonfish_taxonkey"));
```

Now create a temporary table from the **mergedDf** dataframe. We need this table because we are going to copy the results from it into a new **external table** we are creating below. You can check whether **non_fish_temp** was created by using `sqlContext.sql("show tables from jwaller").show();`.

```
mergedDf.createOrReplaceTempView("non_fish_temp");
```




