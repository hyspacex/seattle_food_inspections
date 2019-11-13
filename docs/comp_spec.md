﻿﻿# Component Specification
## Software Components
### 1. Getting Data and cleaning data
We want to keep up-to-date with the latest food inspection scores. This means that we need to keep up with the latest CSV file from King County. We call this function GetData()```def GetData(url=default_url):	return pd.read_csv(url)```We also have to aggregate data and clean the data. Since the dataset will have several entries for the various locations, we want to get the latest data.```def LatestData(data_set):	latest_entries  = []	for rest_location in data_set:		# find the latest health inspection score for this location in the data set		# add this health inspection to the latest entry. 	return cleaned_data```We also have to get location information from a data entry.```def GetLocationRestaraunt(data_set, restaurant) return data_set[restaurant][location]```
### 2. Mapping Data
We have to plot the data.
```
def MakeMap(data, filters)
  plot(location for data subject to filters)
  # filters include various constraints
  return Map
```
### 3. Prediction Modeling (Time Permitting)
(Since this is something that we'll do if time permits, we'll leave this mostly blank for now.)

Broadly speaking we want to have something like [this][1].
## Interactions
As of now we don't know if it will be better to aggregate the data based on zip code or census block. It will depend on the ease of use for each data set.Broadly speaking, in the getting and cleaning data sections we'll build the functionality necessary to map the data properly.

We are considering interactions that would filter our map given selections on corresponding histograms and charts. For example, if we had a correlation figure (scatter plot) that demonstrated the trend between median income and food safety rating, a user could select a group of points and those points would be filtered on the map. Depending on the package suite we end up using, the interactions might be more simple dropdown and radio button filters, informed by static visuals of the data. These might take the form:
```
def MultiSelect()
  select points based on x and y encoding

def MakeHistorgram()
  plot demographic v. food safety rating
  return Hist

add MultiSelect() to Hist

filter Map based on MultiSelect
```

For radio buttons or dropdown, the pseudo code would be similar, but the selection would take the form:
```
def MultiSelect(list)
  dropdown menu with entries from list
```
## Plan Outline
A rough outline is as follows:* Clean the restaurant data and start performing some simple statistical tests on the set* Link the restaurant data with some of the census location information	* Include in this connections between demographic information and census location data* Map the data, and have radio buttons/dropdown menus in order to filter the restaurants by quality, or location associated with census information[1]: https://www.foodqualityandsafety.com/article/predictive-model-sets-priorities-for-chicago-restaurant-inspections/
