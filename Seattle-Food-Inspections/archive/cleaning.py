# -*- coding: utf-8 -*-
"""
cleaning takes the information from the american community survey
and obtains the information taht is necessary for the project.
"""


import pandas as pd




# Creates a marital status data frame
DF_MARITAL = pd.read_csv(
    "../data/raw_data/Marital_Status_ACS_17_5YR_S1201_with_ann.csv")

print(DF_MARITAL.head())
#print(DF_MARITAL.columns)
#print(DF_MARITAL.describe())
#print(DF_MARITAL.info())
#print(DF_MARITAL.shape)

DF_MARITAL2 = DF_MARITAL[['GEO_id2', 'HC01_EST_VC01', 'HC02_EST_VC01',
                          'HC03_EST_VC01', 'HC04_EST_VC01', 'HC05_EST_VC01',
                          'HC06_EST_VC01']]
DF_MARITAL3 = DF_MARITAL2.iloc[1:]
DF_MARITAL3.columns = ['zipcode', 'Population', 'No_Married', 'Widowed',
                       'Divorced', 'Separated', 'Never_Married']
DF_MARITAL3['No_Married'] = int(DF_MARITAL3['No_Married']) / 100

DF_MARITAL3.loc[DF_MARITAL3['No_Married'].str.contains('-'), 'No_Married'] = 0
DF_MARITAL3 = DF_MARITAL3.apply(pd.to_numeric)

'''
ss=['No_Married', 'Widowed', 'Divorced', 'Separated', 'Never_Married']
for j in ss:
    for i in DF_MARITAL3[j]:
        i=i*DF_MARITAL3['Population']
    print(DF_MARITAL3[j])
'''
DF_MARITAL3['No_Married1'] = (DF_MARITAL3['No_Married']
                              * DF_MARITAL3['Population'])
DF_MARITAL3['Widowed1'] = DF_MARITAL3['Widowed'] * DF_MARITAL3['Population']
DF_MARITAL3['Divorced1'] = DF_MARITAL3['Divorced'] * DF_MARITAL3['Population']
DF_MARITAL3['Separated1'] = DF_MARITAL3['Separated'] * DF_MARITAL3['Population']
DF_MARITAL3['Never_Married1'] = (DF_MARITAL3['Never_Married']
                                 * DF_MARITAL3['Population'])

DF_MARITAL3.columns = ['zipcode', 'Population', 'No_Married(%)', 'Widowed(%)',
                       'Divorced(%)', 'Separated(%)', 'Never_Married(%)',
                       'No_Married', 'Widowed', 'Divorced', 'Separated',
                       'Never_Married']

DF_INCOME = pd.read_csv(
    "../data/raw_data/Median_Household_Income_ACS_17_5YR_S1903_with_ann.csv")

print(DF_INCOME.head())
#print(DF_INCOME.columns)
#print(DF_INCOME.describe())
#print(DF_INCOME.info())
#print(DF_INCOME.shape)

DF_INCOME2 = DF_INCOME[['GEO.id2', 'HC01_EST_VC02', 'HC02_EST_VC02',
                        'HC03_EST_VC02']]
DF_INCOME3 = DF_INCOME2.iloc[1:]
DF_INCOME3.columns = ['zipcode', 'Number_Households',
                      'Precent_Distribution_Housesholds',
                      'Median_Income_Households']

DF_INCOME3.loc[DF_INCOME3['No_Married'].str.contains('-'),
               'No_Married'] = DF_INCOME3['Number_Households'].mean()
DF_INCOME3 = DF_INCOME3.apply(pd.to_numeric)


###Joining
DF = pd.merge(left=DF_MARITAL3, right=DF_INCOME3, left_on='zipcode',
              right_on='zipcode')


print(DF_MARITAL.isnull().sum())
#print(DF_MARITAL.isnull().values.any())

DF.to_csv('"../data/raw_data/trial.csv')

DF_FOOD = pd.read_csv("../data/raw_data/Food_Establishment_Inspection_Data.csv")

DF_FOOD['Zip Code'] = DF_FOOD['Zip Code'].astype(str).str.zfill(5)

ZIP_FOOD = list(DF_FOOD['Zip Code'].values())

'''
for i in ZIP_FOOD:
    if i in DF.zipcode:
        print(i)
'''


DF['zipcode'].isin(DF_FOOD['Zip Code']).value_counts()
