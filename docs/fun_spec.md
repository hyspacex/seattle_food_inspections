# Function Design
## Background


Starting 2012, jurisdictions across the country including King County have begun publishing health inspection scores using a standardized scoring system called LIVES. This open data allowed restaurant consumers to make informed decisions based on where they want to eat and motivated a lot of restaurant establishments to improve their inspection score in the hopes of attracting a bigger customer base.

With this data and data from the Census Bureau's American Community survey we’d like to:

* Analyze trends.
* View region specific information.
* Build an interactive map to view correlation between demographic information and restaurant inspection scores.


## User Profile


The user for this project should now how to use tools such as:

* Radio buttons, dropdown menus.
* A JupyterLab notebook, but not proficiency in Python is needed.
* Map programs like Google Maps.


## Data Sources


The data comes from two sources: King County and the Census Bureau's American Community survey.

The data can be found here:

* [King County Washington Food Establishment Data][1]
* American Community Survey data sets:
    * [Data source 1][2]
    * [Data source 2][3]


## Use Cases

### 1. Mapping Restaurants with Food Inspection Scores

Google Maps does not overlay the latest health inspection scores when you search for restaurants online. This seems like useful information someone might need. We image a user wanting to search a map for nearby restaurants, but also see how the restaurant did on the latest health inspection test.

A user can create a map with the function `make_folium_map()` which creates an explorable map to accomplish the above task. When the user has zoomed into a region of a sufficiently small size (which depends on the density of nearby restaurants) the user can see what health scores a restaurant has. 

### 2. Linking Restaurants with Demographic Information in the Surrounding Area

One example use case is to visually see if food inspection ratings are correlated with various demographic information in the city. This is a visual tool analogous to a [study][4] conducted in Ethiopia. The study found an association between food handling practices and various demographic markers such as income or marital status. Related demographic information is tracked by the US Census Bureau.

The objective of the user is to visually relate food inspection scores with census information in the surrounding zip code. The user will make the map (in a JupyterLab notebook) by using the function `make_altair_map(cenus_metric)` where `census_metric` is either the string `'income'` or the string `'married'`. The user will then hover over a location to see the food inspection score, or will select a histogram bar to only see locations with a certain food inspection score. The `census_metric` is included in the background of the map.




[1]: https://data.kingcounty.gov/Health-Wellness/Food-Establishment-Inspection-Data/f29f-zza5
[2]: https://data.census.gov/cedsci/table?q=S1903&table=S1903&tid=ACSST1Y2018.S1903&lastDisplayedRow=0
[3]: https://data.census.gov/cedsci/table?q=S1201&table=S1201&tid=ACSST1Y2018.S1201&lastDisplayedRow=0
[4]: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4057591/
