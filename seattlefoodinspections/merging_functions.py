'''
Python functions to merge the census and food inspection data.
'''

import pandas as pd

def merge_dataframes(df_1, df_2, merge_on):
    '''
    Merges two dataframes on the common column named merge_on.
    '''
    new_df = pd.merge(left=df_1, right=df_2, left_on=merge_on,
                      right_on=merge_on)
    return new_df
