'''
Cleans and combines the census and INSPECTION data.
'''
#Import statements
import pandas as pd
from . import cleaning_functions as cf
from . import merging_functions as mf

#Constants
NAME = 'Name'
CITY = 'City'
VIOLATIONTYPE = 'Violation Type'
ZIPCODE = 'zipcode'
ZIPCODESPACE = 'Zip Code'
LONGITITUDE = 'Longitude'
INSPECTDATE = 'Inspection Date'
RESTAURANTNAME = 'Program Identifier'
ADDRESS = 'Address'
GRADE = 'Grade'
GEOID = 'GEO.id2'
HC01 = 'HC01_EST_VC01'
HC02 = 'HC02_EST_VC01'
HC03 = 'HC03_EST_VC01'
HC04 = 'HC04_EST_VC01'
HC05 = 'HC05_EST_VC01'
HC06 = 'HC06_EST_VC01'
POPULATION = 'Population'
MARRIED = 'No_Married(%)'
WIDOWED = 'Widowed(%)'
DIVORCED = 'Divorced(%)'
SEPARATED = 'Separated(%)'
NEVERMARRIED = 'Never_Married(%)'
MARRIEDTOT = 'No_Married'
WIDOWEDTOT = 'Widowed'
DIVORCEDTOT = 'Divorced'
SEAPARATEDTOT = 'Separated'
NEVERMARRIEDTOT = 'Never_Married'
HOUSEHOLDS = 'Number_Households'
PERDISTHOUSE = 'Percent_Distribution_Housesholds'
MEDINCOME = 'Median_Income_Households'
SERIAL = 'Inspection_Serial_Num'
VIOLATIONID = 'Violation_Record_ID'
PHONE = 'Phone'
PROGID = 'Program Identifier'
MARITAL_CENSUS = './data/raw_data/Marital_ACS_17_5YR_S1201_with_ann.csv'
INCOME_CENSUS = './data/raw_data/Income_ACS_17_5YR_S1903_with_ann.csv'
FOOD_INSPECTION = './data/raw_data/Food_Establishment_INSPECTION.csv'
INSPECTION_OUTPUT = './data/clean_data/clean_inspection.csv'
CENSUS_OUTPUT = './data/clean_data/clean_census.csv'
COMBINED_OUTPUT = './data/clean_data/combined.csv'
SEATTLEZIPS = [98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109,
               98112, 98115, 98116, 98117, 98118, 98119, 98121, 98122, 98125,
               98126, 98133, 98134, 98136, 98144, 98146, 98154, 98155, 98164,
               98168, 98174, 98177, 98178, 98195, 98199]

### Marital dataframe creation
DF_MARITAL = pd.read_csv(MARITAL_CENSUS)
# Removes the top row, which is useless
DF_MARITAL = cf.remove_row_from_data_frame(DF_MARITAL)
# Extracts and rename the proper columns
DF_MARITAL = cf.dataframe_with_columns(DF_MARITAL,
                                       [GEOID, HC01, HC02, HC03, HC04, HC05,
                                        HC06],
                                       [ZIPCODE, POPULATION, MARRIED, WIDOWED,
                                        DIVORCED, SEPARATED, NEVERMARRIED])
# Defining an oft used list of column names.
PERCENT_COLUMNS = [MARRIED, WIDOWED, DIVORCED, SEPARATED, NEVERMARRIED]
# Remove dashes from the data
DF_MARITAL = cf.remove_dashes_from_data(DF_MARITAL, PERCENT_COLUMNS)
# Turns the percents to floats and the population number to an int
DF_MARITAL = cf.columns_to_float(DF_MARITAL, PERCENT_COLUMNS)
DF_MARITAL = cf.columns_to_int(DF_MARITAL, [POPULATION, ZIPCODE])
# Defining another colection of column names.
RAW_TOT_COLUMNS = [MARRIEDTOT, WIDOWEDTOT, DIVORCEDTOT, SEAPARATEDTOT,
                   NEVERMARRIEDTOT]
# Create the new columns which contain the raw totals for all the
# statistics in the marriage center.
DF_MARITAL = cf.data_from_percents_and_raw_totals(DF_MARITAL, PERCENT_COLUMNS,
                                                  POPULATION, RAW_TOT_COLUMNS)
DF_MARITAL = cf.columns_to_int(DF_MARITAL, RAW_TOT_COLUMNS)



### INCOME INFORMATION
DF_INCOME = pd.read_csv(INCOME_CENSUS)
# Remove an extra row
DF_INCOME = cf.remove_row_from_data_frame(DF_INCOME)
# Extract the useful rows
DF_INCOME = cf.dataframe_with_columns(DF_INCOME,
                                      [GEOID, HC01, HC02, HC03],
                                      [ZIPCODE, HOUSEHOLDS,
                                       PERDISTHOUSE,
                                       MEDINCOME])
# Remove dashes from the data, sets them as zero.
DF_INCOME = cf.remove_dashes_from_data(DF_INCOME,
                                       [HOUSEHOLDS,
                                        PERDISTHOUSE,
                                        MEDINCOME])
# zipcode to integer for merging purposes
DF_INCOME = cf.columns_to_int(DF_INCOME, [ZIPCODE])

### Food INSPECTION data frame creation
INSPECTION = pd.read_csv(FOOD_INSPECTION,
                         low_memory=False)
#rename columns for consistency
INSPECTION.rename(columns={ZIPCODESPACE: ZIPCODE}, inplace=True)
# convert dates in 'INSPECTION Date' to date time
INSPECTION[INSPECTDATE] = pd.to_datetime(INSPECTION[INSPECTDATE])
# sort by INSPECTION date then remove duplicates
INSPECTION = INSPECTION.sort_values(
    by=[INSPECTDATE]
).drop_duplicates(subset=[RESTAURANTNAME, ADDRESS], keep='last')
# dropping unnecessary columns
INSPECTION = INSPECTION.drop(
    columns=[
        SERIAL,
        VIOLATIONID,
        PHONE,
        PROGID
    ]
)
# drop na/nan values in appropriate columns
INSPECTION_CLEANED = INSPECTION.dropna(subset=[LONGITITUDE])
INSPECTION_CLEANED = INSPECTION_CLEANED.dropna(subset=[GRADE])
INSPECTION_CLEANED = INSPECTION_CLEANED.dropna(subset=[ZIPCODE])
INSPECTION_CLEANED = INSPECTION_CLEANED.dropna(subset=[NAME])
INSPECTION_CLEANED = INSPECTION_CLEANED.dropna(subset=[CITY])
INSPECTION_CLEANED = INSPECTION_CLEANED.dropna(subset=[VIOLATIONTYPE])
INSPECTION_CLEANED = INSPECTION_CLEANED.sort_values(by=[INSPECTDATE])
# Capitalizing the columns to prevent duplication in enumerating
INSPECTION_CLEANED[CITY] = INSPECTION_CLEANED[CITY].str.upper()
INSPECTION_CLEANED[NAME] = INSPECTION_CLEANED[NAME].str.upper()
INSPECTION_CLEANED[VIOLATIONTYPE] = INSPECTION_CLEANED[VIOLATIONTYPE].str.upper()
# convert the data type of Zip Code to integer
INSPECTION_CLEANED[ZIPCODE] = INSPECTION_CLEANED[ZIPCODE].astype(int)
INSPECTION_ZIPS = INSPECTION_CLEANED[
    INSPECTION_CLEANED[ZIPCODE].isin(SEATTLEZIPS)]
INSPECTION_ZIPS.to_csv(INSPECTION_OUTPUT, index=False)



##COMBINE DATAFRAMES
# first, combine census data
DF_TOTAL = mf.merge_dataframes(DF_MARITAL, DF_INCOME, ZIPCODE)
#output combined census data
DF_TOTAL.to_csv(CENSUS_OUTPUT, index=False)

# next, combine census data with food inspection dataset
COMBINED = mf.merge_dataframes(INSPECTION_ZIPS, DF_TOTAL, ZIPCODE)
COMBINED.to_csv(COMBINED_OUTPUT, index=False)
