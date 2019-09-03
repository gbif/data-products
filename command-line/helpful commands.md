
Here are some file manipulation commands that a useful for preping custom requests. 

replace all commas with empty string  
```
sed -i "s/,//g" test.txt
```

replace all tabs with commas 
```
sed -i "s/\t/,/g" test.txt
```

split file into parts
```
split -l 7000000 pollinators2019.txt pollinators2019_ -d
```
> 

zip a file recursively

grab certain columns from a tsv file and save as new file
awk -F$'\t' '{print $1}' test.txt > test2.txt


