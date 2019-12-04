import folium
from folium import plugins
import altair as alt
import geopandas as gpd
import json

# Create a map centered on Canlis in Seattle, WA
m = folium.Map(
        tiles='Stamen Toner',
        location=[47.6, -122.346742],
        zoom_start = 11
        )

# cluster points
marker_cluster = folium.plugins.MarkerCluster().add_to(m)

# Add marker for each restaurant in the database
for i, r in inspection_cleaned.tail(1200).iterrows():
    folium.Marker(
        # pull lat and lon from entry and use as coordinates for the marker
        location=[r['Latitude'],r['Longitude']],
        # use the business name as the pop
        popup='Restaurant: '+str(r['Inspection Business Name'])+
               '<br>Rating: '+str(r['Inspection Result'])+
                '<br>Date: '+str(r['Inspection Date']),
        icon=folium.Icon()
    ).add_to(marker_cluster)

# Display m
m

seattlezip_geojson = 'https://raw.githubusercontent.com/seattleio/seattle-boundaries-data/master/data/zip-codes.geojson'
gdf = gpd.read_file(seattlezip_geojson)

# merge combined data with geojson
# first, rename zip code column in geojson data set and change to int
gdf.rename(columns={'ZCTA5CE10': 'Zip Code'}, inplace=True)
gdf['Zip Code']=gdf['Zip Code'].astype(int)
combined_geo = gdf.merge(census, on='Zip Code', how='inner')

# transform back to geojson
chloro_json = json.loads(combined_geo.to_json())
chloro_data = alt.Data(values=chloro_json['features'])

alt.data_transformers.enable('json')

# restructure as function, where one can input the column to reference for the chloropleth

def make_visual():
    # interaction, select bar from historgram
    multi = alt.selection_multi(encodings = ['x'],resolve = 'intersect')

    # Seattle background
    background = alt.Chart(chloro_data).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).encode(
        color=alt.Color('properties.Median_Income_Households:Q',
                        scale=alt.Scale(domain=(50000, 150000))),
        tooltip=['properties.Zip Code:Q', 'properties.Median_Income_Households:Q']
    ).properties(
        width=600,
        height=600)

    # add a few restaurants
    sorted10 = inspection_zips.head(5000)
    restaurants = alt.Chart(sorted10).mark_circle().encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        tooltip=['Inspection Business Name','Grade'],
        color=alt.Color('Grade:N',legend=None)
    ).transform_filter(multi)

    # histogram of inspection results
    hist = alt.Chart(sorted10).mark_bar().encode(
        x = 'Grade:N',
        y = 'count()',
        color = 'Grade:N')


    hist_select = alt.layer(
        hist.add_selection(multi).encode(color=alt.value('lightgrey')),
        hist.transform_filter(multi)
    )

    return background + restaurants | hist_select
