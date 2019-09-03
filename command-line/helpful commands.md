
Here are some file manipulation commands that a useful for preping custom requests. 

replace all commas with empty string  
```
sed -i 's/,//g' test.txt
```

replace all tabs with commas 
```
sed -i 's/\t/,/g' test.txt
```

split file into parts 7000000 is the number of lines 
```
split -l 7000000 pollinators2019.txt pollinators2019_ -d
```
> 

zip a file recursively

grab columns 1 and 13 from a tsv file and save as new file 
```
awk -F$'\t' '{print $1"\t"$13}' test.txt > test2.txt
```

add a header to a large file in place
```
sed -i '1i gbifId,scientificName,decimalLatitude,decimalLongitude' test.csv
```
