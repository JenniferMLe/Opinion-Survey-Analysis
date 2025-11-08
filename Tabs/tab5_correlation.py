import utils
import streamlit as st
import plotly.express as px
import pandas as pd
from scipy.stats import chi2_contingency
import math 

df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    correlation = st.container()

    with correlation:
        filter1,filter2,blank = st.columns([1,1,2]) 
        with filter1: year = st.slider('year',2020,2025,value=2022)
        with filter2: weighted = st.radio('',['Use weighted data', 'Use raw data'],horizontal=True)
        df = df_combined[df_combined['Year']==year]

        sm = ['Facebook', 'Youtube', 'Twitter', 'Instagram', 'Snapchat',
            'Whatsapp', 'Linkedin', 'Pinterest', 'Tiktok', 'Bereal', 'Reddit']
        
        metrics = ['Econ_Rating','Econ_Rating_Cat','Econ_Outlook','Econ_Outlook_Cat','Econ_Rating_Outlook']
        all_cors = []
        for metric in metrics:
            cors = []
            for feature in demographics + sm:
                if feature in col:
                    feature = col[feature]
                ct = df
                ct = ct[ct[metric] != 'Refused']
                ct = ct[ct[feature] != 'Refused']

                if weighted == 'Use weighted data':
                    ct = pd.crosstab(ct[feature], ct[metric], values=ct['Weight'], aggfunc='sum')
                else:
                    ct = pd.crosstab(ct[feature], ct[metric])

                if ct.size == 0:
                    cors.append(None)
                    continue

                ct = ct.fillna(0)
                chi2, p, dof, expected = chi2_contingency(ct)

                n = 0
                for c in ct.columns:
                    n += ct[c].sum()

                k = min(len(ct),len(ct.columns))
                cors.append(round(math.sqrt(chi2/(n*(k-1))),2))

            all_cors.append(cors)

            utils.write_to_file(pd.DataFrame(all_cors))

        data = pd.DataFrame(all_cors,index=metrics,columns=demographics+sm)

        fig = px.imshow(data, text_auto=True, title='Correlation Strength (0 to 1) Using Cramer\'s V')

        st.plotly_chart(fig)


        st.markdown('<div class="border">'  
            "- <b>Correlation</b> is the <b>association or dependence</b> between two variables.<br>" 
            "- We'll use <b>Cramer's V</b> to measure correlation since NPORS data is nominal "
            "(categories instead of numbers) and ordinal (categories with rank).<br>"
            "- Cramer's V <b>ranges from 0 to 1</b> with 0 being no dependence and 1 being complete dependence.<br>"
            "- <b>Guideline</b>: ≤ 0.2: weak association, 0.2 < X ≤ 0.6: moderate association, > 0.6: strong assocation"
            ""
        '</div>', unsafe_allow_html=True)