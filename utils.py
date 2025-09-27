import pandas as pd
# import plotly.express as px
import numpy as np

def write_to_file(df,file_name='Datasets/result.csv'):
    df.to_csv(file_name, index=False)

# print a list of distinct values from a column in a dataframe
# helps with data cleaning
def get_distinct_values(df, columns, sort_by):
    vals = df[columns].sort_values(by=sort_by).drop_duplicates()
    # print to csv file to see all values since output may be cut if too long
    write_to_file(vals)

# stop number of columns at the end that don't have the year in the column name
def remove_year_from_column_name(dataset, stop):
    list_columns = list(dataset.columns)

    for i in range(0,len(list_columns)-stop):
        list_columns[i] = list_columns[i][:-5]

    dataset.columns = list_columns

def get_count(cols):
    # as_index=False doesn't make group labels the index
    df = df_combined.groupby(cols, as_index=False)['RESPID'].count()
    df = df.rename(columns={'RESPID':'Count'})
    for col in cols:
        df = df[df[col] != 'N/A']
    write_to_file(df)
    return df

def get_count_weighted(cols):
    # as_index=False doesn't make group labels the index
    df = df_combined.groupby(cols, as_index=False)['WEIGHT'].sum().round(0)
    df = df.rename(columns={'WEIGHT':'Count'})
    for col in cols:
        df = df[df[col] != 'N/A']
    write_to_file(df)
    return df

category_orders = {
    'AGEGRP2':['18-24','25-39','40-59','60-79','80+'],

    'INCOMEGRP':['< $40K','$40-70K','$70-100K','$100K+'],

    'ECON1MOD':['Poor','Only fair','Good','Excellent'],

    'ECON1BMOD':['Better','About the same','Worse'],
    
    'EDUCATION':[
        "No schooling completed",
        "Some High School",
        "High School",
        "Some College",
        "Associate's Degree",
        "Bachelor's Degree",
        "Master's Degree or Higher"
    ]
}

income_map2 = {
    'Under $40k':"#3d005e",
    '$40-70K':"#8a03d5",
    '$70-100K':"#bd45ff",
    '$100K+':"#d995ff"
}