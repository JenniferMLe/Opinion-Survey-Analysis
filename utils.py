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
        column = 'Weight'
        # as_index=False doesn't make group labels the index
        df = df.groupby(cols, as_index=False)[column].sum().round(0)
    else:
        column = 'Respid'
        df = df.groupby(cols, as_index=False)[column].count()
    
    df = df.rename(columns={column:'count'})

    write_to_file(df)
    return df

def get_percent_increase(df,group,problem,weighted):
    if group == 'social_media':
        sm = ['Facebook', 'Youtube', 'Twitter', 'Instagram', 'Snapchat',
            'Whatsapp', 'Linkedin', 'Pinterest', 'Tiktok', 'Bereal', 'Reddit']
        
        cols = ['Respid','Year',problem,'Weight']

        df = df[cols+sm]
        df = pd.melt(df, id_vars=cols,value_vars=sm, var_name='social_media')
        df = df[df['value']=='Use']
    
    df = get_count(df,['Year',group,problem],weighted)

    df = df[(df['Year'] == 2021) | (df['Year'] == 2022)]

    # get the count for each unique year + group + sentiment
    df = df.groupby(['Year',group,problem],as_index=False)['count'].sum()

    # convert to wide format so negative rating counts and positive rating counts are a separate columns
    df = pd.pivot_table(df,index=['Year',group],columns=[problem],values='count').reset_index()

    # add a column for the percent of negative ratings 
    df['PercentNegative'] = round((df['Negative'] / (df['Negative']+df['Positive']))*100,1)

    # convert to wide so each year gets its own column with percent negative as the values
    df = pd.pivot_table(df,index=group,columns='Year',values=['Negative','PercentNegative']).reset_index()

    # column names are tuples since values is a list so convert to string
    new_col_names = []
    for col in df.columns:
        new_col_name = ''
        for x in col:
            new_col_name += str(x)
        new_col_names.append(new_col_name)
    df.columns = new_col_names

    df = df.rename(columns={
        'Negative2021':'n_2021',
        'Negative2022':'n_2022',
        'PercentNegative2021':'percent_2021',
        'PercentNegative2022':'percent_2022'
    })

    df['n_2021'] = df['n_2021'].astype(int)
    df['n_2022'] = df['n_2022'].astype(int)
    df['percent_2021'] = round(df['percent_2021'],0).astype(int)
    df['percent_2022'] = round(df['percent_2022'],0).astype(int)
    
    # # calculate the difference between the percent of negative ratings for the current and previous year
    df['percent_diff'] = round(df['percent_2022'] - df['percent_2021'],0).astype(int)

    write_to_file(df)
    return df