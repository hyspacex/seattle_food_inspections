'''
functions for visualizing food inspection and census dataset
'''
import pandas as pd
import folium
from folium import plugins
import altair as alt
import geopandas as gpd
import json

def make_folium_map():
    DATA = pd.read_csv('./data/clean_data/combined.csv',
                            low_memory=False)
    m = folium.Map(
            tiles='Stamen Toner',
            location=[47.6, -122.346742],
            zoom_start = 11
            )

    # cluster points
    marker_cluster = folium.plugins.MarkerCluster().add_to(m)

    # Add marker for each restaurant in the database
    for i, r in DATA.tail(1200).iterrows():
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
    return m

def make_altair_map():
    # import inspection dataset
    INSPECTION = pd.read_csv('./data/clean_data/combined.csv',
                            low_memory=False)
    #import seattle zip codes
    SEATTLEZIP_GEOJSON = 'https://raw.githubusercontent.com/seattleio/seattle-boundaries-data/master/data/zip-codes.geojson'
    GDF = gpd.read_file(SEATTLEZIP_GEOJSON)
    # merge combined data with geojson
    # first, rename zip code column in geojson data set and change to int
    GDF.rename(columns={'ZCTA5CE10': 'zipcode'}, inplace=True)
    GDF['zipcode']=GDF['zipcode'].astype(int)
    combined_geo = GDF.merge(INSPECTION, on='zipcode', how='left')

    # transform back to geojson
    CHLORO_JSON = json.loads(combined_geo.to_json())
    CHLORO_DATA = alt.Data(values=CHLORO_JSON['features'])

    alt.data_transformers.enable('json')

    # interaction, select bar from historgram
    multi = alt.selection_multi(encodings = ['x'],resolve = 'intersect')

    # Seattle background
    background = alt.Chart(CHLORO_DATA).mark_geoshape(
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
    RESTAURANTS = INSPECTION.head(5000)
    restaurants = alt.Chart(RESTAURANTS).mark_circle().encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        tooltip=['Inspection Business Name','Grade'],
        color=alt.Color('Grade:N',legend=None)
    ).transform_filter(multi)

    # histogram of inspection results
    hist = alt.Chart(RESTAURANTS).mark_bar().encode(
        x = 'Grade:N',
        y = 'count()',
        color = 'Grade:N')


    hist_select = alt.layer(
        hist.add_selection(multi).encode(color=alt.value('lightgrey')),
        hist.transform_filter(multi)
    )

    return background + restaurants | hist_select
