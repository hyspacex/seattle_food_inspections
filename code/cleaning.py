# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 10:29:16 2019

@author: mfardhossein
"""


import pandas as pd
import matplotlib.pyplot as plt





df_martial=pd.read_csv("C:/Users/mfardhossein/Documents/CS_583/project/Marital_Status_ACS_17_5YR_S1201/ACS_17_5YR_S1201_with_ann.csv")

print(df_martial.head())
#print(df_martial.columns)
#print(df_martial.describe())
#print(df_martial.info())
#print(df_martial.shape)

df_martial2 = df_martial[['GEO_id2', 'HC01_EST_VC01', 'HC02_EST_VC01', 'HC03_EST_VC01', 'HC04_EST_VC01','HC05_EST_VC01','HC06_EST_VC01']]
df_martial3= df_martial2.iloc[1:]
df_martial3.columns =['zipcode', 'Population', 'No_Married', 'Widowed','Divorced','Separated','Never_Married']
df_martial3['No_Married'] = int(df_martial3['No_Married']) /100

df_martial3.loc[df_martial3['No_Married'].str.contains('-'), 'No_Married']=0
df_martial3 = df_martial3.apply(pd.to_numeric)

'''
ss=['No_Married', 'Widowed','Divorced','Separated','Never_Married']
for j in ss:
    for i in df_martial3[j]:
        i=i*df_martial3['Population']        
    print(df_martial3[j])
'''
df_martial3['No_Married1']= df_martial3['No_Married'] * df_martial3['Population']
df_martial3['Widowed1']= df_martial3['Widowed'] * df_martial3['Population']
df_martial3['Divorced1']= df_martial3['Divorced'] * df_martial3['Population']
df_martial3['Separated1']= df_martial3['Separated'] * df_martial3['Population']
df_martial3['Never_Married1']= df_martial3['Never_Married'] * df_martial3['Population']

df_martial3.columns =['zipcode', 'Population', 'No_Married(%)', 'Widowed(%)','Divorced(%)','Separated(%)','Never_Married(%)', 'No_Married', 'Widowed','Divorced','Separated','Never_Married']

df_income=pd.read_csv("C:/Users/mfardhossein/Documents/CS_583/project/Median_Household_Income_ACS_17_5YR_S1903/ACS_17_5YR_S1903_with_ann.csv")

print(df_income.head())
#print(df_income.columns)
#print(df_income.describe())
#print(df_income.info())
#print(df_income.shape)

df_income2 = df_income[['GEO.id2', 'HC01_EST_VC02', 'HC02_EST_VC02', 'HC03_EST_VC02']]
df_income3= df_income2.iloc[1:]
df_income3.columns =['zipcode', 'Number_Households', 'Precent_Distribution_Housesholds', 'Median_Income_Households']

df_income3.loc[df_income3['No_Married'].str.contains('-'), 'No_Married']=df_income3['Number_Households'].mean()
df_income3 = df_income3.apply(pd.to_numeric)


###Joining
df = pd.merge(left=df_martial3, right=df_income3, left_on='zipcode', right_on='zipcode')


print(df_martial.isnull().sum())
#print(df_martial.isnull().values.any())

df.to_csv('C:/Users/mfardhossein/Documents/CS_583/project/Marital_Status_ACS_17_5YR_S1201/trial.csv')

df_food=pd.read_csv("C:/Users/mfardhossein/Documents/CS_583/project/Food_Establishment_Inspection_Data (3).csv")

df_food['Zip Code']= df_food['Zip Code'].astype(str).str.zfill(5)

zip_food = list(df_food['Zip Code'].values())

'''
for i in zip_food:
    if i in df.zipcode:
        print(i)
'''


df['zipcode'].isin(df_food['Zip Code']).value_counts()