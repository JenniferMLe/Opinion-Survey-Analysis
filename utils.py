import pandas as pd
# import plotly.express as px
import numpy as np

def write_to_file(df,file_name='Datasets/result.csv'):
    df.to_csv(file_name, index=False)
# print a list of distinct values from a column in a dataframe
# helps with data cleaning
def get_distinct_values(df, columns):
    vals = df[columns].unique()
    return vals
    # print to csv file to see all values since output may be cut if too long
    # write_to_file(vals)

# stop number of columns at the end that don't have the year in the column name
def remove_year_from_column_name(dataset, stop):
    list_columns = list(dataset.columns)

    for i in range(0,len(list_columns)-stop):
        list_columns[i] = list_columns[i][:-5]

    dataset.columns = list_columns

def get_count(df,cols):
    # as_index=False doesn't make group labels the index
    df = df.groupby(cols, as_index=False)['RESPID'].count()
    df = df.rename(columns={'RESPID':'Count'})
    for col in cols:
        df = df[df[col] != 'N/A']
    write_to_file(df)
    return df

def get_count_weighted(df,cols):
    # as_index=False doesn't make group labels the index
    df = df.groupby(cols, as_index=False)['WEIGHT'].sum().round(0)
    df = df.rename(columns={'WEIGHT':'Count'})
    for col in cols:
        df = df[df[col] != 'N/A']
    write_to_file(df)
    return df

def get_percent_increase(df,column,weighted=True):
    if weighted: df = get_count_weighted(df,['YEAR',column,'ECON1MOD'])
    else: df = get_count(['YEAR',column,'ECON1MOD'])

    conditions = [
        (df['ECON1MOD'] == 'Excellent') | (df['ECON1MOD'] == 'Good'),
        (df['ECON1MOD'] == 'Poor') | (df['ECON1MOD'] == 'Only fair')
    ]
    group = ['Positive', 'Negative']

    # create a new column that labels each rating as negative or positive
    df['SENTIMENT'] = np.select(conditions, group, default='N/A')

    # get the count for each unique year + group + sentiment
    df = df.groupby(['YEAR',column,'SENTIMENT'],as_index=False)['Count'].sum()

    # convert to wide format so negative rating counts and positive rating counts are a separate columns
    df = pd.pivot_table(df,index=['YEAR',column],columns=['SENTIMENT'],values='Count').reset_index()

    # add a column for the percent of negative ratings 
    df['PercentNegative'] = round((df['Negative'] / (df['Negative']+df['Positive']))*100,1)

    # convert to wide so each year gets its own column with percent negative as the values
    df = pd.pivot_table(df,index=column,columns='YEAR',values='PercentNegative').reset_index()
    
    # calculate the difference between the percent of negative ratings for the current and previous year
    # 
    col_names = []
    for year in df.columns[2:]:
        col_name = str(year)
        df[col_name] = round(df[year] - df[year-1],1)
        col_names.append(col_name)
    
    # exclude all columns but the group name and the percent difference columns
    df = df[[column]+col_names]
    
    # convert back to long format so we can graph by Year
    df = pd.melt(df,id_vars = [column], value_vars=col_names,var_name='YEAR',value_name='PercentNegDiff')
    write_to_file(df)
    return df