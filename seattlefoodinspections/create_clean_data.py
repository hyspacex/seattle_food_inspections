'''
Cleans and combines the census and INSPECTION data.
'''
#Import statements
import pandas as pd
from . import cleaning_functions as cf
from . import merging_functions as mf

#Constants
ZIPCODE = 'zipcode'
LONGITITUDE = 'Longitude'
INSPECTDATE = 'Inspection Date'
RESTAURANTNAME = 'Program Identifier'
ADDRESS = 'Address'
GRADE = 'Grade'
SEATTLEZIPS = [98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109,
               98112, 98115, 98116, 98117, 98118, 98119, 98121, 98122, 98125,
               98126, 98133, 98134, 98136, 98144, 98146, 98154, 98155, 98164,
               98168, 98174, 98177, 98178, 98195, 98199]

### Marital dataframe creation
DF_MARITAL = pd.read_csv(
    './data/raw_data/Marital_ACS_17_5YR_S1201_with_ann.csv')
# Removes the top row, which is useless
DF_MARITAL = cf.remove_row_from_data_frame(DF_MARITAL)
# Extracts and rename the proper columns
DF_MARITAL = cf.dataframe_with_columns(DF_MARITAL,
                                       ['GEO.id2', 'HC01_EST_VC01',
                                        'HC02_EST_VC01', 'HC03_EST_VC01',
                                        'HC04_EST_VC01', 'HC05_EST_VC01',
                                        'HC06_EST_VC01'],
                                       ['zipcode', 'Population',
                                        'No_Married(%)', 'Widowed(%)',
                                        'Divorced(%)', 'Separated(%)',
                                        'Never_Married(%)'])
# Defining an oft used list of column names.
PERCENT_COLUMNS = ['No_Married(%)', 'Widowed(%)', 'Divorced(%)', 'Separated(%)',
                   'Never_Married(%)']
# Remove dashes from the data
DF_MARITAL = cf.remove_dashes_from_data(DF_MARITAL, PERCENT_COLUMNS)
# Turns the percents to floats and the population number to an int
DF_MARITAL = cf.columns_to_float(DF_MARITAL, PERCENT_COLUMNS)
DF_MARITAL = cf.columns_to_int(DF_MARITAL, ['Population', 'zipcode'])
# Defining another colection of column names.
RAW_TOT_COLUMNS = ['No_Married', 'Widowed', 'Divorced', 'Separated',
                   'Never_Married']
# Create the new columns which contain the raw totals for all the
# statistics in the marriage center.
DF_MARITAL = cf.data_from_percents_and_raw_totals(DF_MARITAL, PERCENT_COLUMNS,
                                                  "Population",
                                                  RAW_TOT_COLUMNS)
DF_MARITAL = cf.columns_to_int(DF_MARITAL, RAW_TOT_COLUMNS)



### INCOME INFORMATION
DF_INCOME = pd.read_csv("./data/raw_data/Income_ACS_17_5YR_S1903_with_ann.csv")
# Remove an extra row
DF_INCOME = cf.remove_row_from_data_frame(DF_INCOME)
# Extract the useful rows
DF_INCOME = cf.dataframe_with_columns(DF_INCOME,
                                      ['GEO.id2', 'HC01_EST_VC02',
                                       'HC02_EST_VC02', 'HC03_EST_VC02'],
                                      ['zipcode', 'Number_Households',
                                       'Percent_Distribution_Housesholds',
                                       'Median_Income_Households'])
# Remove dashes from the data, sets them as zero.
DF_INCOME = cf.remove_dashes_from_data(DF_INCOME,
                                       ['Number_Households',
                                        'Percent_Distribution_Housesholds',
                                        'Median_Income_Households'])
# zipcode to integer for merging purposes
DF_INCOME = cf.columns_to_int(DF_INCOME, ['zipcode'])

### Food INSPECTION data frame creation
INSPECTION = pd.read_csv('./data/raw_data/Food_Establishment_INSPECTION.csv',
                         low_memory=False)
#rename columns for consistency
INSPECTION.rename(columns={'Zip Code': ZIPCODE}, inplace=True)
# convert dates in 'INSPECTION Date' to date time
INSPECTION[INSPECTDATE] = pd.to_datetime(INSPECTION[INSPECTDATE])
# sort by INSPECTION date then remove duplicates
INSPECTION = INSPECTION.sort_values(
    by=[INSPECTDATE]
).drop_duplicates(subset=[RESTAURANTNAME, ADDRESS], keep='last')
# drop na/nan values in appropriate columns
INSPECTION_CLEANED = INSPECTION.dropna(subset=[LONGITITUDE])
INSPECTION_CLEANED = INSPECTION_CLEANED.dropna(subset=[GRADE])
INSPECTION_CLEANED = INSPECTION_CLEANED.dropna(subset=[ZIPCODE])
INSPECTION_CLEANED = INSPECTION_CLEANED.sort_values(by=[INSPECTDATE])
# convert the data type of Zip Code to integer
INSPECTION_CLEANED[ZIPCODE] = INSPECTION_CLEANED[ZIPCODE].astype(int)
INSPECTION_ZIPS = INSPECTION_CLEANED[INSPECTION_CLEANED[ZIPCODE
].isin(SEATTLEZIPS)]
INSPECTION_ZIPS.to_csv('./data/clean_data/clean_inspection.csv', index=False)



##COMBINE DATAFRAMES
# first, combine census data
DF_TOTAL = mf.merge_dataframes(DF_MARITAL, DF_INCOME, 'zipcode')
#output combined census data
DF_TOTAL.to_csv('./data/clean_data/clean_census.csv', index=False)

# next, combine census data with food inspection dataset
COMBINED = mf.merge_dataframes(INSPECTION_ZIPS, DF_TOTAL, ZIPCODE)
COMBINED.to_csv('./data/clean_data/combined.csv', index=False)
