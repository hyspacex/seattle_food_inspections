'''
functions for visualizing food inspection and census dataset
'''

import json
import pandas as pd
import folium
from folium import plugins
import altair as alt
import geopandas as gpd

def make_folium_map():
    '''
    function for making folium map of seattle restaurants that can be zoomed
    and navigated
    '''
    map_data = pd.read_csv('./data/clean_data/combined.csv',
                           low_memory=False)
    folium_map = folium.Map(
        tiles='Stamen Toner',
        location=[47.6, -122.346742],
        zoom_start=11)

    # cluster points
    marker_cluster = folium.plugins.MarkerCluster().add_to(folium_map)

    # Add marker for each restaurant in the database
    for index, row in map_data.tail(1200).iterrows():
        folium.Marker(
            # pull lat and lon from entry and use as coordinates for the marker
            location=[row['Latitude'], row['Longitude']],
            # use the business name as the pop
            popup='Restaurant: '+str(row['Inspection Business Name'])+
            '<br>Rating: '+str(row['Inspection Result'])+
            '<br>Date: '+str(row['Inspection Date']),
            icon=folium.Icon()
        ).add_to(marker_cluster)

    # Display map
    return folium_map

def make_altair_map():
    '''
    function to make altair chlorpleth map based on census data overlayed
    with retaurants colored by their food inspection grade
    '''
    # import inspection dataset
    inspection = pd.read_csv('./data/clean_data/combined.csv',
                             low_memory=False)
    #import seattle zip codes
    seattlezip_geojson = 'https://raw.githubusercontent.com/seattleio/seattle'\
                          '-boundaries-data/master/data/zip-codes.geojson'
    gdf = gpd.read_file(seattlezip_geojson)
    # merge combined data with geojson
    # first, rename zip code column in geojson data set and change to int
    gdf.rename(columns={'ZCTA5CE10': 'zipcode'}, inplace=True)
    gdf['zipcode'] = gdf['zipcode'].astype(int)
    combined_geo = gdf.merge(inspection, on='zipcode', how='left')

    # transform back to geojson
    chloro_json = json.loads(combined_geo.to_json())
    chloro_data = alt.Data(values=chloro_json['features'])

    alt.data_transformers.enable('json')

    # interaction, select bar from historgram
    multi = alt.selection_multi(encodings=['x'], resolve='intersect')

    # Seattle background
    background = alt.Chart(chloro_data).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).encode(
        color=alt.Color('properties.Median_Income_Households:Q',
                        scale=alt.Scale(domain=(50000, 150000))),
        tooltip=['properties.zipcode:Q', 'properties.Median_Income_Households:Q']
    ).properties(
        width=600,
        height=600)

    # add a few restaurants
    restaurant_grades = inspection.head(5000)
    restaurants = alt.Chart(restaurant_grades).mark_circle().encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        tooltip=['Inspection Business Name', 'Grade'],
        color=alt.Color('Grade:N', legend=None)
    ).transform_filter(multi)

    # histogram of inspection results
    hist = alt.Chart(restaurant_grades).mark_bar().encode(
        x='Grade:N',
        y='count()',
        color='Grade:N')


    hist_select = alt.layer(
        hist.add_selection(multi).encode(color=alt.value('lightgrey')),
        hist.transform_filter(multi)
    )

    return background + restaurants | hist_select
