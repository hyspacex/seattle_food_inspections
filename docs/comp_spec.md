﻿﻿﻿
## Software Components
### 1. Getting Data and cleaning data
We want to keep up-to-date with the latest food inspection scores. This means that we need to keep up with the latest CSV file from King County. We call this function GetData()

We have to plot the data.
```

  plot(location for data subject to filters)
  # filters include various constraints
  return Map
```
### 3. Prediction Modeling (Time Permitting)
(Since this is something that we'll do if time permits, we'll leave this mostly blank for now.)

Broadly speaking we want to have something like [this][1].



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
