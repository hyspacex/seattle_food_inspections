'''
Python code to clean the census data.
'''

import pandas as pd

def dataframe_with_columns(data_frame, columns_list, new_names):
    '''
    Extracts certain columns from the dataframe and changes the names of
    the columns
    '''
    data_frame_subset = data_frame[columns_list] #extracts columns
    data_frame_subset.columns = new_names #renames columns
    return data_frame_subset


def remove_row_from_data_frame(data_frame):
    '''
    Removes the top row from a dataframe.
    '''
    return data_frame.iloc[1:]

def remove_dashes_from_data(data_frame, cols):
    '''
    Remove the dashes from the dataset, but only
    looks at the columns in "cols"
    '''
    for col_name in cols:
        vec = list(data_frame[col_name])
        for vec_local, vec_elem in enumerate(vec):
            if vec_elem == "-":
                vec[vec_local] = 0
        data_frame[col_name] = vec
    return data_frame

def columns_to_float(data_frame, col):
    '''
    Convertes a collection of columns in a dataframe to a
    float type.
    '''
    for col_name in col:
        data_frame[col_name] = [float(f) for f in data_frame[col_name]]
    return data_frame

def columns_to_int(data_frame, col):
    '''
    Convertes a collection of columns in a dataframe to a
    int type.
    '''
    for col_name in col:
        data_frame[col_name] = [int(f) for f in data_frame[col_name]]
    return data_frame

def data_from_percents_and_raw_totals(data_frame, column_list,
                                      tot_row, new_list):
    '''
    The dataframe contains information of percents (in the column_list) and
    a total variable (in tot_row). This creates new columns (labeled by
    new_list) which is the row-wise product of percent and total variable.
    '''
    col_length = len(column_list)
    for j in range(0, col_length):
        data_frame[new_list[j]] = (data_frame[column_list[j]]
                                   * data_frame[tot_row]) / 100
    return data_frame

def merge_dataframes(df_1, df_2, merge_on):
    '''
    Merges two dataframes on the common column named merge_on.
    '''
    new_df = pd.merge(left=df_1, right=df_2, left_on=merge_on,
                      right_on=merge_on)
    return new_df
