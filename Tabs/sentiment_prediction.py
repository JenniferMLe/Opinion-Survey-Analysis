import utils
import streamlit as st
import plotly.express as px
import pandas as pd
from scipy.stats import chi2_contingency
import math 

# create local constants from utils so we don't have to keep doing util.
df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    correlation = st.container()

    # create heapmap showing the correlation strength between each feature and metric
    with correlation:
        filter1,filter2,blank = st.columns([1,1,2]) 
        with filter1: year = st.slider('year',2020,2025,value=2022)
        with filter2: weighted = st.radio('',['Use weighted data', 'Use raw data'],horizontal=True)
        df = df_combined[df_combined['Year'] == year]
        
        metrics = ['Econ_Rating','Econ_Outlook','Econ_Rating_Outlook']
        # contains all correlation strenghts for each feature and metric
        all_cors = []
        for metric in metrics:
            # correlation strength for all features and metric
            cors = []
            for feature in demographics + social_media:
                # if feature is a demographic and needs to be translated to column name
                if feature in col:
                    feature = col[feature]

                ct = df
                ct = ct[ct[metric] != 'Refused']
                ct = ct[ct[feature] != 'Refused']

                # create contingency table (frequency for each feature and metric value)
                if weighted == 'Use weighted data':
                    ct = pd.crosstab(ct[feature], ct[metric], values=ct['Weight'], aggfunc='sum')
                else:
                    ct = pd.crosstab(ct[feature], ct[metric])

                # if feature doesn't exist for the given year
                if ct.size == 0:
                    cors.append(None)
                    continue
                
                # fill Null values with 0 to prevent Null chi2
                ct = ct.fillna(0)

                # get chi2 value using contingency table
                chi2, p, dof, expected = chi2_contingency(ct)

                # get the sum of all values in contingency table
                n = 0
                for c in ct.columns:
                    n += ct[c].sum()

                # k is the minimum categories between metric and feature categories
                k = min(len(ct),len(ct.columns))

                # compute cramer's v value and append to correlation list
                cors.append(round(math.sqrt(chi2/(n*(k-1))),2))

            all_cors.append(cors)

        data = pd.DataFrame(all_cors,index=metrics,columns=demographics+social_media)

        # create heapmap displaying correrlation strength
        fig = px.imshow(data, text_auto=True, title='Correlation Strength (0 to 1) Using Cramer\'s V')

        st.plotly_chart(fig)

        st.markdown('<div class="border">'  
            "- <b>Correlation</b> is the <b>association or dependence</b> between two variables.<br>" 
            "- We will use <b>Cramer's V</b> to measure correlation since NPORS data is nominal "
            "(categories instead of numbers) and ordinal (categories with rank).<br>"
            "- Cramer's V <b>ranges from 0 to 1</b> with 0 being no dependence and 1 being complete dependence.<br>"
            "- <b>Guideline</b>: ≤ 0.2: weak association, 0.2 < X ≤ 0.6: moderate association, > 0.6: strong assocation"
            ""
        '</div>', unsafe_allow_html=True)