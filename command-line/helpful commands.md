
Here are some file manipulation commands that a useful for preping custom requests. 

replace all commas with empty string  
```
sed -i "s/,//g" test.txt
```

replace all tabs with commas 
```
sed -i "s/\t/,/g" test.txt
```

split file into 
```
split -l 7000000 pollinators2019.txt pollinators2019_ -d
```

zip a file recursively


