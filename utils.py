import pandas as pd
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

def get_count(df,cols,weighted):
    if weighted:
        column = 'WEIGHT'
        # as_index=False doesn't make group labels the index
        df = df.groupby(cols, as_index=False)[column].sum().round(0)
    else:
        column = 'RESPID'
        df = df.groupby(cols, as_index=False)[column].count()
    
    df = df.rename(columns={column:'Count'})

    for col in cols:
        df = df[df[col] != 'N/A']

    write_to_file(df)
    return df

def get_percent_increase(df,group,problem,weighted):
    df = get_count(df,['YEAR',group,'ECON1MOD','ECON1BMOD'],weighted)
    df = df[(df['YEAR'] == 2021) | (df['YEAR'] == 2022)]

    if problem == 'ECON1MOD':
        conditions = [
            (df['ECON1MOD'] == 'Excellent') | (df['ECON1MOD'] == 'Good'),
            (df['ECON1MOD'] == 'Poor') | (df['ECON1MOD'] == 'Only fair')
        ]
    elif problem == 'ECON1BMOD':
        conditions = [
            (df['ECON1BMOD'] == 'Better'),
            (df['ECON1BMOD'] == 'Worse')
        ]
    else:
        conditions = [
            ((df['ECON1BMOD'] == 'Better') | ((df['ECON1BMOD'] == 'About the same') & (df['ECON1MOD'].isin(['Good','Excellent'])))),
            ((df['ECON1BMOD'] == 'Worse') | ((df['ECON1BMOD'] == 'About the same') & (df['ECON1MOD'].isin(['Poor','Only fair']))))
        ]
    sentiment = ['Positive', 'Negative']

    # create a new column that labels each rating as negative or positive
    df['SENTIMENT'] = np.select(conditions, sentiment, default='N/A')

    # get the count for each unique year + group + sentiment
    df = df.groupby(['YEAR',group,'SENTIMENT'],as_index=False)['Count'].sum()

    # convert to wide format so negative rating counts and positive rating counts are a separate columns
    df = pd.pivot_table(df,index=['YEAR',group],columns=['SENTIMENT'],values='Count').reset_index()

    # add a column for the percent of negative ratings 
    df['PercentNegative'] = round((df['Negative'] / (df['Negative']+df['Positive']))*100,1)

    # convert to wide so each year gets its own column with percent negative as the values
    df = pd.pivot_table(df,index=group,columns='YEAR',values='PercentNegative').reset_index()
    
    # calculate the difference between the percent of negative ratings for the current and previous year
    df['PercentNegDiff'] = round(df[2022] - df[2021],1)
    df = df[[group,'PercentNegDiff']]

    write_to_file(df)
    return df