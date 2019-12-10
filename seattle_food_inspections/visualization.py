'''
functions for visualizing food inspection and census dataset
'''
import os
import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster # pylint: disable=unused-import
import altair as alt
import geopandas as gpd

def make_folium_map(boo_val=False):
    '''
    function for making folium map of seattle restaurants that can be zoomed
    and navigated.

    Args:
        boo_val (boolean): default value is false, used to output a folium map
                           when True
    '''
    map_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "./data/clean_data/combined.csv"),
                           low_memory=False)
    # associate color with inspection result
    map_data['marker_color'] = map_data['Grade']
    map_data['marker_color'] = map_data['marker_color'].replace([1.0], 'lightgreen')
    map_data['marker_color'] = map_data['marker_color'].replace([2.0], 'orange')
    map_data['marker_color'] = map_data['marker_color'].replace([3.0], 'red')
    map_data['marker_color'] = map_data['marker_color'].replace([4.0], 'black')

    folium_map = folium.Map(
        tiles='Stamen Toner',
        location=[47.6, -122.346742],
        zoom_start=11)

    # cluster points
    marker_cluster = folium.plugins.MarkerCluster().add_to(folium_map)

    # Add marker for each restaurant in the database
    for _, row in map_data.iterrows():
        folium.Marker(
            # pull lat and lon from entry and use as coordinates for the marker
            location=[row['Latitude'], row['Longitude']],
            # use the business name as the pop
            popup='<b>Restaurant</b>: '+str(row['Inspection Business Name']) +
            '<br><b>Result from most recent inspection</b>: ' +
            str(row['Inspection Result']) +
            '<br><b>Overall Grade</b>: ' + str(row['Grade']) +
            '<br><b>Date</b>: ' + str(row['Inspection Date']),
            icon=folium.Icon(color=row['marker_color'])
        ).add_to(marker_cluster)
    display = folium_map.save("map.html")
    if boo_val:
        output = folium_map
    else:
        output = display
    return output

def make_altair_map(census_metric):
    '''
    function to make altair chlorpleth map based on census data overlayed
    with retaurants colored by their food inspection grade

    Args:
        census_metric (str): which census metric to plot on base map_data
            one of ('income', 'married')

    Returns:
        interactive map
    '''

    #set certain constaints
    gcolor = 'oranges' # color scale for inspection grade

    if not census_metric in ['income', 'married']:
        raise ValueError('Your input is not one of [income] or [married]')

    if census_metric == 'income':
        metric = 'properties.Median_Income_Households'
    elif census_metric == 'married':
        metric = 'properties.No_Married(%)'



    # import inspection dataset
    inspection = pd.read_csv(os.path.join(os.path.dirname(__file__), "./data/clean_data/combined.csv"),
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
        color=alt.Color(metric, type='quantitative',
                        scale=alt.Scale(scheme='lighttealblue'),
                        legend=alt.Legend(orient='left')),
        tooltip=[alt.Tooltip('properties.zipcode', type='ordinal'),
                 alt.Tooltip(metric, type='quantitative')]
    ).properties(
        width=600,
        height=600)

    # add restaurants
    restaurant_grades = inspection.head(5000)
    restaurants = alt.Chart(restaurant_grades).mark_circle().encode(
        longitude='Longitude:Q',
        latitude='Latitude:Q',
        tooltip=['Inspection Business Name', 'Grade'],
        color=alt.Color('Grade:O',
                        legend=None,
                        scale=alt.Scale(scheme=gcolor, domain=(4, 3, 2, 1))
                        )
    ).transform_filter(multi)

    # histogram of inspection results
    hist = alt.Chart(restaurant_grades).mark_bar().encode(
        x='Grade:O',
        y='count()',
        color=alt.Color('Grade:O',
                        legend=None,
                        scale=alt.Scale(scheme=gcolor, domain=(4, 3, 2, 1))
                        )
        )

    # add selection function to histogram and base the filter on the selection
    hist_select = alt.layer(
        hist.add_selection(multi).encode(color=alt.value('lightgrey')),
        hist.transform_filter(multi)
    )

    return background + restaurants | hist_select
