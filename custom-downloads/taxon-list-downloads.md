# Long taxonkey list download

Sometimes users want to download a lot of taxon keys like >40K in some cases. This is not possible to do over via the website or using curl or something like that. Note this is mostly for internal use and a regular user will not be able to do this. 


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



