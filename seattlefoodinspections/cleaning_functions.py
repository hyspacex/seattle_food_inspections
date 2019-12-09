'''
Python code to clean the census and food inspection data.
'''

def dataframe_with_columns(data_frame, columns_list, new_names):
    '''
    Extracts certain columns from the dataframe and changes the names of
    the columns

    Args:
        data_frame (dataframe): dataframe to be cleaned
        columns_list (list of str): list of columns to keep in output
        new_names (list of str): list of desired column names for output

    Returns:
        data_frame_subset: cleaned dataframe
    '''
    data_frame_subset = data_frame[columns_list] #extracts columns
    data_frame_subset.columns = new_names #renames columns
    return data_frame_subset


def remove_row_from_data_frame(data_frame):
    '''
    Removes the top row from a dataframe.

    Args:
        data_frame (dataframe): dataframe to be cleaned

    Returns:
        data_frame: cleaned dataframe
    '''
    return data_frame.iloc[1:]

def remove_dashes_from_data(data_frame, col):
    '''
    Remove the dashes from the dataset, but only
    looks at the columns in "cols"

    Args:
        data_frame (dataframe): dataframe to be cleaned
        col (list of str): list of columns to be cleaned

    Returns:
        data_frame: cleaned dataframe
    '''
    for col_name in col:
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

    Args:
        data_frame (dataframe): dataframe to be cleaned
        col (list of str): list of columns to be cleaned

    Returns:
        data_frame: cleaned dataframe
    '''
    for col_name in col:
        data_frame[col_name] = [float(f) for f in data_frame[col_name]]
    return data_frame

def columns_to_int(data_frame, col):
    '''
    Convertes a collection of columns in a dataframe to a
    int type.

    Args:
        data_frame (dataframe): dataframe to be cleaned
        col (list of str): list of columns to be cleaned

    Returns:
        data_frame: cleaned dataframe
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

    Args:
        data_frame (dataframe): dataframe to be cleaned
        column_list (list of str): list of columns to be cleaned
        tot_row (str): column that contains total values
        new_list (list of str): list of column names 

    Returns:
        data_frame: cleaned dataframe
    '''
    col_length = len(column_list)
    for j in range(0, col_length):
        data_frame[new_list[j]] = (data_frame[column_list[j]]
                                   * data_frame[tot_row]) / 100
    return data_frame
