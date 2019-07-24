# Long taxonkey list download

Sometimes users want to download a lot of taxon keys like >40K in some cases. This is not possible to do over via the website or using curl or something like that. If the taxonkey list is less than around 5K [see dicussion here](https://github.com/ropensci/rgbif/issues/362) then it is probably easier to do a download using a http GET request. It might also be possible to break up big downloads into 5K-taxonkey chunks, but if even that is too many downloads. A taxonkey list custom download might be warrented. 
 
# Making a long taxonkey list download 

Step 1. Get your taxonkey list


