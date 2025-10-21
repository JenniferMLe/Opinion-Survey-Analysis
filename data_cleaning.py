import utils
import pandas as pd
import numpy as np

def import_and_combine_datatsets():
    # Save each .sav as a data frame
    df_20 = pd.read_spss("Datasets/NPORS-2020/dataset.sav")
    df_21 = pd.read_spss("Datasets/NPORS-2021/dataset.sav")
    df_22 = pd.read_spss("Datasets/NPORS-2022/dataset.sav")
    df_23 = pd.read_spss("Datasets/NPORS-2023/dataset.sav")
    df_24 = pd.read_spss("Datasets/NPORS-2024/dataset.sav")
    df_25 = pd.read_spss("Datasets/NPORS-2025/dataset.sav")

    # convert .sav to .csv
    utils.write_to_file(df_20,"Datasets/NPORS-2020/dataset_20.csv")
    utils.write_to_file(df_21,"Datasets/NPORS-2021/dataset_21.csv")
    utils.write_to_file(df_22,"Datasets/NPORS-2022/dataset_22.csv")
    utils.write_to_file(df_23,"Datasets/NPORS-2023/dataset_23.csv")
    utils.write_to_file(df_24,"Datasets/NPORS-2024/dataset_24.csv")
    utils.write_to_file(df_25,"Datasets/NPORS-2025/dataset_25.csv")
    print('imnport success')

    # Remove the year from column name to keep naming consistant
    utils.remove_year_from_column_name(df_20, 5)
    utils.remove_year_from_column_name(df_21, 2)

    # ensure columns recording the same data have the same name
    # so there aren't duplicate columns when appending datasets
    df_20 = df_20.rename(columns={
        'SEXASK':'GENDER', 
        'EDUC_ACS':'EDUCATION',
        'REGION_NAME':'REGION'
    })
    df_21 = df_21.rename(columns={

    })
    df_22 = df_22.rename(columns={
        'CREGION':'REGION'
    })

    df_23 = df_23.rename(columns={
        'BASEWT':'BASEWEIGHT', 
        'INC_SDT1':'INCOME',
        'CREGION':'REGION'
    })

    df_24 = df_24.rename(columns={
        'BASEWT':'BASEWEIGHT', 
        'INC_SDT1': 'INCOME',
        'SMUSEa' : 'SMUSE_a','SMUSEd' : 'SMUSE_d','SMUSEg' : 'SMUSE_g','SMUSEj' : 'SMUSE_j',
        'SMUSEb' : 'SMUSE_b','SMUSEe' : 'SMUSE_e','SMUSEh' : 'SMUSE_h','SMUSEk' : 'SMUSE_k',
        'SMUSEc' : 'SMUSE_c','SMUSEa' : 'SMUSE_f','SMUSEi' : 'SMUSE_i',
        'CREGION':'REGION'
    })

    df_25 = df_25.rename(columns={
        'BASEWT':'BASEWEIGHT', 
        'INC_SDT1': 'INCOME',
        'CREGION':'REGION'
    })

    # add year columns to all datasets
    df_20['YEAR'] = 2020
    df_21['YEAR'] = 2021
    df_22['YEAR'] = 2022
    df_23['YEAR'] = 2023
    df_24['YEAR'] = 2024
    df_25['YEAR'] = 2025

    # Combine (append) all datasets together
    df_combined = pd.concat([df_20, df_21, df_22, df_23, df_24, df_25])
    print('Combining datasets successful')
    return df_combined

def remove_and_rename_columns(df_combined):
    # Keep relevent columns only
    df_combined = df_combined[[
        'RESPID','YEAR','AGE','AGEGRP','GENDER','RACECMB', # basic demographics
        'INCOME','EDUCATION', 'REGION','RELIG', 'PARTY', # other useful demographics 
        'RELIMP', 'PRAY', 'MARITAL', # other features
        'SMUSE_a', 'SMUSE_b', 'SMUSE_c', 'SMUSE_d', 'SMUSE_e', 'SMUSE_f', # social media use
        'SMUSE_g','SMUSE_h','SMUSE_i','SMUSE_j','SMUSE_k',
        'ECON1MOD', 'ECON1BMOD', # we want to study how this changes over time
        'BASEWEIGHT', 'WEIGHT' # weights 
    ]]
    # rename columns
    df_combined = df_combined.rename(columns={
        'SMUSE_a':'FACEBOOK',
        'SMUSE_b':'YOUTUBE',
        'SMUSE_c':'TWITTER',
        'SMUSE_d':'INSTAGRAM',
        'SMUSE_e':'SNAPCHAT',
        'SMUSE_f':'WHATSAPP',
        'SMUSE_g':'LINKEDIN',
        'SMUSE_h':'PINTEREST',
        'SMUSE_i':'TIKTOK',
        'SMUSE_j':'BEREAL',
        'SMUSE_k':'REDDIT',
        'RACECMB':'RACE'
    })
    print('Removing and renaming columns successful')
    return df_combined

def replace_values(df_combined):
    # change n/a to -1 so we can convert age to float
    df_combined["AGE"] = df_combined["AGE"].replace({
        "n/a":"-1",
        "98+":"98",
        "":"-1",
        'Refused':"-1"
    })

    # change column type
    df_combined["AGE"] = df_combined["AGE"].astype(float)

    df_combined = df_combined.replace({
        r'.*Refused.*':'N/A', 
        r'.*Something else.*':'Other',
        'No, don\'t use this':'No use',
        # 'No, dont use this':'No use',
        "Yes, use this":'Yes use',
    },regex=True)

    df_combined['GENDER'] = df_combined['GENDER'].replace({
        "A man":"Male",
        "A woman":"Female",
        "In some other way":"Other"
    })

    df_combined["RACE"] = df_combined["RACE"].replace({
        r'.*Asian.*':'Asian',
        r'.*Black.*':'Black',
        r'.*other.*':'Other',
        'Mixed race':'Mixed Race'
    },regex=True)

    df_combined['ECON1MOD'] = df_combined['ECON1MOD'].replace('Only Fair','Only fair')

    df_combined["INCOME"] = df_combined["INCOME"].replace({
        r' to less than ':'-',
        r' or more':'+',
        r'Less than':'<',
        r',000':'K',
    },regex=True)

    df_combined["EDUCATION"] = df_combined["EDUCATION"].replace({
        r'.*11.*':'Some High School',
        r'.*12.*':'Some High School',
        r'.*high school.*':'High School',
        r'.*GED.*':'High School',
        r'.*college.*':'Some College',
        r'.*Associate.*':'Associate\'s Degree',
        r'.*Bachelor.*':'Bachelor\'s Degree',
        r'.*Master.*':'Master\'s Degree or Higher',
        r'.*MD.*':'Master\'s Degree or Higher',
        r'.*Doctorate.*':'Master\'s Degree or Higher',
        'Kindergarten':'N/A'
    },regex=True)

    df_combined["RELIG"] = df_combined["RELIG"].replace({
        r'.*Mormon.*':'Mormon',
        r'.*Orthodox.*':'Orthodox',
        r'.*Protestant.*':'Protestant'
    },regex=True)

    df_combined['MARITAL'] = df_combined['MARITAL'].replace({
        "Separated":"Divorced",
        "Never been married":"Never married",
    })

    categorical_cols = df_combined.select_dtypes(include="category").columns
    df_combined[categorical_cols] = df_combined[categorical_cols].astype(str)
    return df_combined

def create_calculated_columns(df_combined):
    # conditions for each group
    conditions = [
        df_combined['INCOME'].isin(['$10K-$20K','$20K-$30K','$30K-$40K','< $10K','< $30K']),
        df_combined['INCOME'].isin(['$40K-$50K','$50K-$60K','$60K-$70K','$50K-$70K']),
        df_combined['INCOME'].isin(['$70K-$100K','$70K-$80K','$70K-$90K','$75K-$100K','$80K-$90K','$90K-$100K']),
        df_combined['INCOME'].isin(['$100K+','$100K-$125K','$100K-$150K','$125K-$150K','$150K+'])
    ]
    # corresponding groups for each condition
    group = ['< $40K','$40-70K','$70-100K','$100K+']

    # insert new column after INCOME
    df_combined.insert(
        df_combined.columns.get_loc('INCOME') + 1, # position we want to insert at
        'INCOMEGRP', # name of new column
        np.select(conditions, group, default='N/A') # set value according to conditions 
    )

    '''create calculated columns to group incomes'''
    conditions = [
        (df_combined['AGEGRP'] == '18-24') | ((18 <= df_combined['AGE']) & (df_combined['AGE'] <= 24)),
        (df_combined['AGEGRP'].isin(['25-29','30-34','35-39'])) | ((25 <= df_combined['AGE']) & (df_combined['AGE'] <= 39)),
        (df_combined['AGEGRP'].isin(['40-44','45-49','50-54','55-59'])) | ((40 <= df_combined['AGE']) & (df_combined['AGE'] <= 59)),
        (df_combined['AGEGRP'].isin(['60-64','65-69','70-74','75-79'])) | ((60 <= df_combined['AGE']) & (df_combined['AGE'] <= 79)),
        (df_combined['AGEGRP'] == '80+')| (80 <= df_combined['AGE'])
    ]
    group = ['18-24','25-39','40-59','60-79','80+']

    df_combined.insert(
        df_combined.columns.get_loc('AGEGRP') + 1, # position we want to insert at
        'AGEGRP2', # name of new column
        np.select(conditions, group, default='N/A') # set value according to conditions 
    )
    return df_combined

df_combined = import_and_combine_datatsets()
df_combined = remove_and_rename_columns(df_combined)
df_combined = replace_values(df_combined)
df_combined = create_calculated_columns(df_combined)

utils.write_to_file(df_combined, 'Datasets/combined_dataset.csv')
utils.write_to_file(df_combined.iloc[0:100])
print('DATA CLEANING SUCCESSFUL')