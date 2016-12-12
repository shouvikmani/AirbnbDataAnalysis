# Investigating the Airbnb Marketplace in New York City
##### Aatish Nayak (aatishn) + Shouvik Mani (shouvikm)

### Running our code
As explained in the notebook, the data collection code is encapsulated in one file `airbnb-client.py`
You can run the `airbnb-client.py` script in this directory by running the following command:
```
$ python airbnb-client.py "<location>:<location1>:<location2>" <num_results> <output_filename>
```
`location#` is the location in which to search for Airbnbs. 
Examples:
```
$ python airbnb-client.py "Manhattan, New York" 500
$ python airbnb-client.py "Manhattan, New York:Queens, New York:Bronx, New York:Staten Island, New York:Brooklyn, New York" 1000
```
If no output file is specified, the output is saved to `airbnb-results.csv`.
The script also uses `params.txt` that contains a new line seperated list of parameters to extract for each listing. Take a look at our `params.txt` to see what we extract.

### Data Sources
Save these and correct the pathnames in the notebook code to import the data.
[NYC Borough Shapefiles](http://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nybb_16d.zip) used to create maps of regions and determine mean prices for each borough.
[Zillow Rent Data](http://files.zillowstatic.com/research/public/Neighborhood/Neighborhood_MedianRentalPrice_1Bedroom.csv) for comparison to Airbnb prices
[Third Party Airbnb API](http://airbnbapi.org/) to collect all the data.


