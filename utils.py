import pandas as pd
import numpy as np

def write_to_file(df,file_name='Datasets/result.csv'):
    df.to_csv(file_name, index=False)

# print a list of distinct values from a column in a dataframe
# helps with data cleaning
def get_distinct_values(df, columns):
    vals = df[columns].unique()
    vals = pd.DataFrame(vals)
    write_to_file(vals)
    return vals

def get_count(df,cols,weighted):
    if weighted:
        column = 'WEIGHT'
        # as_index=False doesn't make group labels the index
        df = df.groupby(cols, as_index=False)[column].sum().round(0)
    else:
        column = 'RESPID'
        df = df.groupby(cols, as_index=False)[column].count()
    
    df = df.rename(columns={column:'count'})

    write_to_file(df)
    return df

def get_percent_increase(df,group,problem,weighted):
    if group == 'social_media':
        sm = ['FACEBOOK','YOUTUBE','TWITTER','INSTAGRAM','SNAPCHAT','WHATSAPP',
                'LINKEDIN','PINTEREST','TIKTOK','BEREAL','REDDIT']
        cols = ['RESPID','YEAR','ECON1MOD','ECON1BMOD','WEIGHT']

        df = df[cols+sm]
        df = pd.melt(df, id_vars=cols,value_vars=sm, var_name='social_media')
        df = df[df['value']=='Use']
    
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
    df['SENTIMENT'] = np.select(conditions, sentiment, default='Refused')

    # get the count for each unique year + group + sentiment
    df = df.groupby(['YEAR',group,'SENTIMENT'],as_index=False)['count'].sum()

    # convert to wide format so negative rating counts and positive rating counts are a separate columns
    df = pd.pivot_table(df,index=['YEAR',group],columns=['SENTIMENT'],values='count').reset_index()

    # add a column for the percent of negative ratings 
    df['PercentNegative'] = round((df['Negative'] / (df['Negative']+df['Positive']))*100,1)

    # convert to wide so each year gets its own column with percent negative as the values
    df = pd.pivot_table(df,index=group,columns='YEAR',values=['Negative','PercentNegative']).reset_index()

    # column names are tuples since values is a list so convert to string
    new_col_names = []
    for col in df.columns:
        new_col_name = ''
        for x in col:
            new_col_name += str(x)
        new_col_names.append(new_col_name)
    df.columns = new_col_names

    df = df.rename(columns={
        'Negative2021':'2021_Count',
        'Negative2022':'2022_Count',
        'PercentNegative2021':'2021_Percent',
        'PercentNegative2022':'2022_Percent'
    })

    df['2021_Count'] = df['2021_Count'].astype(int)
    df['2022_Count'] = df['2022_Count'].astype(int)
    df['2021_Percent'] = round(df['2021_Percent'],0).astype(int)
    df['2022_Percent'] = round(df['2022_Percent'],0).astype(int)
    
    
    # # calculate the difference between the percent of negative ratings for the current and previous year
    df['PercentDiff'] = round(df['2022_Percent'] - df['2021_Percent'],0).astype(int)

    write_to_file(df)
    return df
