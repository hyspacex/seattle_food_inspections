﻿
# Component Specification

## Software Components

### 1. Cleaning data


We have to aggregate and clean the data. The Census data contains a lot more information than is need for this project, and that information is spread throughout several datasets. The Census data also has customized column labels, that are essentially meaningless for our project. For this problem we have to extract desired columns from a dataset by:

```
def dataframe_with_columns(data_frame, columns_list, new_names):
    data_frame_subset = data_frame[columns_list] #extracts columns
    data_frame_subset.columns = new_names #renames columns
    return data_frame_subset
```
The above takes a data frame named `data_frame` extracts the columns with names in `columns_list` and then renames those columns by `new_names`.


Some of the numerical data in the Census is not in the correct format we either want or need. For example, empty numerical values in the Census data are indicated by `-` which should be converted to `0`. We do this by:
```
def remove_dashes_from_data(data_frame, col):
    for col_name in col:
        vec = list(data_frame[col_name])
        if vec[j] == "-":
            do: vec[j] = 0
        data_frame[col_name] = vec
    return data_frame
```
The above code just changes `-` values to `0` values. 

We also need functions to accomplish the following tasks:
* Convert dataframe columns from type `int` to type `float` (and vice-versa).
* Remove unnecessary rows from a dataframe
* Convert a percentage information to a raw total information.


### 2. Merging Data

Once the data is cleaned, we have to merge the various data sources. This is done by something like
```
def merge_dataframes(census_1, census_2, food):
    census_tot = merge(census_1, census_2, column='zipcode')
    # merge the census data at the dataframe column named 'zipcode'
    return merge(census_tot, food, column = 'zipcode')
```

This will likely involve renaming columns so that the `census_1`, `census_2`, and `food` have a common column named `'zipcode'`.




### 3. Mapping Data


We have to plot the data. We do this in two ways. We create a `folium` map which includes only the food inspection score information. This is done by
```
def make_folium_map():
    plot(local, color)
    #color is a product of the health inspection score at local
    return map
```

In order to utilize this connection with census demographic information, we use `altair`. We create a function of the form:
```
def make_altair_map(census_metric)
    hist(food_score) 
    #create a histogram showing total frequency of food_scores
    color zipcodes by census_metric frequency
    plot(restaurant locations linked with food scores)
    return map
```


### 4. Example Notebook

We create an example `JupyterLab` notebook that allows the user to plot and interact with the maps. 


## Interactions

The way the above components interact to accomplish the use case follows in a simple chain. In order to use the notebooks, i.e. for the user to use the product, we must be able to create the maps. In order to create the maps, we need to have the census data linked with the food inspection data. In order to link these data sets in an efficient manner, we have to clean and restrict the data.
## Plan Outline


A rough outline is as follows:

* Clean the restaurant data and start performing some simple statistical tests on the set
* Link the restaurant data with some of the census location information
	* Include in this connections between demographic information and census location data
* Map the data, and have radio buttons/dropdown menus in order to filter the restaurants by quality, or location associated with census information

