
This script will let you export tab delimited file to the custom downloads folder. Make sure to alter jwaller to your user and to zip the file. 

```
spark2-shell 
```

```scala
import org.apache.spark.sql.SaveMode
import sys.process._

val save_table_name = "dbscan_outliers_export"

df_export.
write.format("csv").
option("sep", "\t").
option("header", "false").
mode(SaveMode.Overwrite).
save(save_table_name)

// export and copy file to right location 
(s"hdfs dfs -ls")!
(s"rm " + save_table_name)!
(s"hdfs dfs -getmerge /user/jwaller/"+ save_table_name + " " + save_table_name)!
(s"head " + save_table_name)!
// val header = "1i " + "specieskey\tspecies_occ_count\tdatasetkey\tdataset_occ_count\tdecimallatitude\tdecimallongitude\tgbifid\tbasisofrecord\tkingdom\tclass\tkingdomkey\tclasskey\teventdate\tdatasetname\tdate"
val header = "1i " + df_export.columns.toSeq.mkString("""\t""")
Seq("sed","-i",header,save_table_name).!
(s"rm /mnt/auto/misc/download.gbif.org/custom_download/jwaller/" + save_table_name)!
(s"ls -lh /mnt/auto/misc/download.gbif.org/custom_download/jwaller/")!
(s"cp /home/jwaller/" + save_table_name + " /mnt/auto/misc/download.gbif.org/custom_download/jwaller/" + save_table_name)!
```
