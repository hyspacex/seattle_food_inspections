'''
Cleans the census data.
'''
#Import statements
import pandas as pd

from . import cleaning_functions as cf


### Marital dataframe creation
DF_MARITAL = pd.read_csv(
    "./data/raw_data/Marital_ACS_17_5YR_S1201_with_ann.csv")
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
DF_MARTIAL = cf.columns_to_int(DF_MARITAL, ["Population"])
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



'''
COMBINE DATAFRAMES
'''

DF_TOTAL = cf.merge_dataframes(DF_MARITAL, DF_INCOME, "zipcode")

DF_TOTAL.to_csv("./data/clean_data/clean_census.csv", index=False)
