working with hdfs code snippets

merge all files into one file into local directory

```
hdfs dfs -getmerge /user/jwaller/occ_count_by_country_export.csv occ_count_by_country_export.tsv
```

Get hdfs files that match a string (like "country_counts_"). Useful for snapshot exports. Print command needed to get merge them. 
```
files=$(hdfs dfs -ls -C | grep country_counts_)
for file in $files; do echo "hdfs dfs -getmerge /user/jwaller/$file $file"; done
```


