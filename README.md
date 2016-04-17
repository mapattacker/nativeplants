# nativeplants

### Description
Germplasm Resources Information Network (GRIN) has a large repository of plant related information; giving details like economic uses, common names, and most importantly, the distribution ranges where their native regions are also recorded.

These ranges follow closely to the hierarchical system provided by the International Working Group on Taxonomic Databases for Plant Sciences (TDWG). It is in version 2 now. See more <a href="https://github.com/tdwg/prior-standards/tree/master/world-geographical-scheme-for-recording-plant-distributions">here</a>.

### How it works

The scripts makes use of the above two sources to extract their native distribution:

1) grinscrape.py: Using selenium, input each species name into GRIN's webform and find a match with the region provided by TDWG within their native distribution range. Results are stored in an sqlite database.

2) grinoutput.py: Pulls out total count of each region for each hierarchical level into an csv file. You can write your own SQL output if you require individual species details.

3) Generate world map: Download the shapefiles from Wek Gardens <href="http://www.kew.org/gis/tdwg/index.html">website</a>. Note their licensing criteria. Do a table join with the csv output using the region names to the shapefile attribute table's corresponding name.
