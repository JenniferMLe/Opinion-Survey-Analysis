import pandas as pd

# read cleaned dataset from csv file
df_combined = pd.read_csv('Datasets/combined_dataset.csv')

demographics = ['Age','Race','Gender','Income','Education','Region','Party',
                'Marital Status','Religion','Faith Importance']

social_media = ['Facebook', 'Youtube', 'Twitter', 'Instagram', 'Snapchat',
            'Whatsapp', 'Linkedin', 'Pinterest', 'Tiktok', 'Bereal', 'Reddit']

# maps selection label to column names
col = {
    'Age':'Age_Cat',
    'Race':'Race',
    'Gender':'Gender',
    'Income':'Income_Cat',
    'Region':'Region',
    'Education':'Education',
    'Social Media':'Social_Media',
    'Party':'Party',
    'Religion':'Religion',
    'Faith Importance':'Faith_Importance',
    'Marital Status':'Marital',
    'Economy Rating':'Econ_Rating',
    'Economy Outlook':'Econ_Outlook',
    'Economy Rating and Outlook':'Econ_Rating_Outlook'
}

# define order for categorical columns
category_orders = {
    'Age_Cat':['18-24','25-39','40-59','60-79','80+'],
    'Income_Cat':['< $40K','$40-70K','$70-100K','$100K+'],
    'Econ_Rating':['Poor','Only Fair','Good','Excellent'],
    'Econ_Outlook':['Worse','About the same','Better'],
    'Party':['Democrat','Republican','Independent','Other'],
    'Faith_Importance':['Not at all important','Not too important','Somewhat important','Very important'],
    'Marital':['Never married','Living with a partner','Married','Divorced','Widowed'],
    'Education':[
        "No schooling completed",
        "Some High School",
        "High School",
        "Some College",
        "Associate's Degree",
        "Bachelor's Degree",
        "Master's Degree or Higher"
    ]
}

# define graph colors
colors = [
    "#264653", "#2A9D8F", "#E9C46A",
    "#F4A261", "#E76F51", "#D3D3D3", "#1D3557"
]

# writes a dataframe to a csv filt for debugging
def write_to_file(df,file_name='result.csv'):
    df.to_csv(file_name, index=False)

# print a list of distinct values from a column in a dataframe
# helps with data cleaning
def get_distinct_values(df, columns):
    vals = df[columns].unique()
    vals = pd.DataFrame(vals)
    return vals

# gets count of df grouped by each column in cols
def get_count(df,cols,weighted):
    if weighted:
        column = 'Weight'
        # as_index=False doesn't make group labels the index
        df = df.groupby(cols, as_index=False)[column].sum().round(0)
    else:
        column = 'Respid'
        df = df.groupby(cols, as_index=False)[column].count()
    
    df = df.rename(columns={column:'count'})

    return df

def get_percent_increase(df,dg,metric,weighted):
    if dg == 'Social_Media':
        cols = ['Year',metric,'Weight']
        df = df[cols+social_media]
        df = pd.melt(df, id_vars=cols,value_vars=social_media, var_name='Social_Media')
        df = df[df['value']=='Use']

    df = get_count(df,['Year',dg,metric],weighted)

    df = df[(df['Year'] == 2021) | (df['Year'] == 2022)]

    # get the count for each unique year + group + sentiment
    df = df.groupby(['Year',dg,metric],as_index=False)['count'].sum()

    # convert to wide format so negative rating counts and positive rating counts are separate columns
    df = pd.pivot_table(df,index=['Year',dg],columns=[metric],values='count').reset_index()

    df = df[df[dg] != 'Refused']
    df = df.fillna(0)

    negative = ''
    if metric == 'Econ_Rating':
        # add a column for the percent of negative ratings 
        df['PercentNegative'] = round((df['Poor'] / (df['Poor']+df['Only Fair']+df['Good']+df['Excellent']+df['Refused']))*100,1)
        negative = 'Poor'
    elif metric == 'Econ_Outlook':
        # add a column for the percent of negative ratings 
        df['PercentNegative'] = round((df['Worse'] / (df['Worse']+df['About the same']+df['Better']+df['Refused']))*100,1)
        negative = 'Worse'
    elif metric == 'Econ_Rating_Outlook':
        df['PercentNegative'] = round((df['Negative'] / (df['Negative']+df['Neutral']+df['Positive']+df['Refused']))*100,1)
        negative = 'Negative'
    
    # convert to wide so each year gets its own column with percent negative as the values
    df = pd.pivot_table(df,index=dg,columns='Year',values=[negative,'PercentNegative']).reset_index()

    # column names are tuples since values is a list so convert to string
    new_col_names = []
    for col in df.columns:
        new_col_name = ''
        for x in col:
            new_col_name += str(x)
        new_col_names.append(new_col_name)
    df.columns = new_col_names

    df = df.rename(columns={
        negative+'2021':'n_2021',
        negative+'2022':'n_2022',
        'PercentNegative2021':'percent_2021',
        'PercentNegative2022':'percent_2022'
    })

    df['n_2021'] = df['n_2021'].astype(int)
    df['n_2022'] = df['n_2022'].astype(int)
    df['percent_2021'] = round(df['percent_2021'],0).astype(int)
    df['percent_2022'] = round(df['percent_2022'],0).astype(int)
    
    # # calculate the difference between the percent of negative ratings for the current and previous year
    df['percent_diff'] = round(df['percent_2022'] - df['percent_2021'],0).astype(int)

    return df