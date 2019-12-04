import pandas as pd
import os

inspection = pd.read_csv('./data/raw_data/Food_Establishment_Inspection.csv',low_memory=False)
# convert dates in 'Inspection Date' to date time
inspection['Inspection Date']=pd.to_datetime(inspection['Inspection Date'])
# sort by inspection date then remove duplicates
inspection = inspection.sort_values(by=['Inspection Date']).drop_duplicates(subset = ['Program Identifier', 'Address'], keep = 'last')

inspection_cleaned = inspection.dropna(subset = ['Longitude'])
inspection_cleaned = inspection_cleaned.dropna(subset = ['Grade'])
inspection_cleaned = inspection_cleaned.dropna(subset = ['Zip Code'])
inspection_cleaned = inspection_cleaned.sort_values(by=['Inspection Date'])

# convert the data type of Zip Code to integer
inspection_cleaned['Zip Code']=inspection_cleaned['Zip Code'].astype(int)
inspection_zips = inspection_cleaned[inspection_cleaned['Zip Code'].isin([98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109, 98112, 98115, 98116, 98117, 98118, 98119, 98121, 98122, 98125, 98126, 98133, 98134, 98136, 98144, 98146, 98154, 98164, 98174, 98177, 98178, 98195, 98199])]

# import census data to data frame
census = pd.read_csv('./data/clean_data/clean_census.csv')
# merge inspection and census data by zip code
# first, rename column in census data set
census.rename(columns={'zipcode': 'Zip Code'}, inplace=True)
combined = pd.merge(inspection_zips, census, on='Zip Code', how='left')
