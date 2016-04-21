# nativeplants

### Description

Extract native regions from a list of plant species and make a world map showing their distributions.

### Data Sources

Germplasm Resources Information Network (GRIN) has a large repository of plant related information; giving details like economic uses, common names, and most importantly, the distribution ranges where their native regions are also recorded.

These ranges follow closely to the hierarchical system provided by the International Working Group on Taxonomic Databases for Plant Sciences (TDWG). It is in version 2 now. See more __<a href="https://github.com/tdwg/prior-standards/tree/master/world-geographical-scheme-for-recording-plant-distributions">here</a>__.

Kew Gardens made world maps in shapefile format for each hierarchical level.

### How it works

The scripts makes use of the above two sources to extract their native distribution:

1) __grin.sqlite__: You will need to load the species list into the "species" table, "speciesName" field (note to only put in strictly generic and specific epithet, without the author's name). "nativeto" table holds the output of the scanned data from GRIN, i.e., species is native to which region. Subsequent tables are imported directed from the hierarchical system of plant distribution from TDWG. I have added a new field "Synonym" to both level 3 and level 4 tables to catch some differences in naming convention between TDWG and GRIN.

2) __grinscrape.py__: Using selenium, input each species name into GRIN's webform and find a match with the region provided by TDWG within their native distribution range. Results are stored in an sqlite database.

3) __grinscrape2.py__: The scraping will fail too when the search result more than 1 result. This needs to be decided by the user on which to choose. For such instances, use this modified script. The script will prompt two inputs. First, enter the species in question indicated in sqlite "speciesName". After manually locating the plant species url in GRIN, then input the full url. The script will then update the native distributions in the database.

4) __grinoutput.py__: Pulls out total count of each region for each hierarchical level into an csv file. You can write your own SQL output if you require individual species details.

5) __Generate world map__: Download the shapefiles from Kew Gardens __<a href="http://www.kew.org/gis/tdwg/index.html">website</a>__. Do a table join with the csv output using the region names to the shapefile attribute table's corresponding name. Use a graduated symbology to show a heatmap of the world based on the accumulative native distributions of the plant species.

### Note
It is possible that GRIN uses some other synonyms that I have not accounted for. I will update the database if I find more. 

### License
My scripts are all MIT licensed. However, note that the TDWG data is a "Creative Commons Attribution 4.0 International Public License", and shapefiles are only for non-profit use. Please see their websites from the links provided earlier for more information.
