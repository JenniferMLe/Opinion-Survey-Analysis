import utils
import streamlit as st
import plotly.express as px

# create local constants from utils so we don't have to keep doing util.
df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    st.subheader("Did events in 2022 increase negative sentiment?")    
    
    st.markdown(
        '<div class="border">'  
            "<b>Events happening in 2021 and 2022 could have affected sentiment</b> "
            "such as Joe Biden taking office and rising inflation rates. "

            "<b>Inflation rates</b> represent the increase in prices compared to the previous year. " 
            "At its peak, the 12-month inflation rate was 9.1% in June of 2022 meaning prices on average " 
            "were 9.1% more expensive compared to June of 2021. View inflation rate trends from 2000-current "
            '<a href="https://www.usinflationcalculator.com/inflation/current-inflation-rates/" target="_blank">here. </a>'
        '</div>'
    ,unsafe_allow_html=True)

    st.markdown(
        "Defining the **hypothesis**\n"
        "> - **Null Hypothesis** → 2022 events did not affect opinions. Average Treatment Effect (ATE) = 0\n"
        "> - **Alternative Hypothesis** → 2022 events affected opinions. Average Treament Effect (ATE) ≠ 0\n"
        "> - **Significance level** → 0.05\n"
        "\n>**ATE** tells us how much the outcome would change if everyone experienced 2022 events compared to if " 
        "no one experienced 2022 events. "
        ,unsafe_allow_html=True
    )

    st.markdown(
        "\nUsing **causal inference**, EconML's doubly-robust learner, and the following ... \n"  
        "> - **Control** → Year = 2021\n"
        "> - **Treatment** → Year = 2022\n"
        "> - **Outcome** → Overall Sentiment = 'Negative'\n"
        "> - **Covariates** → variables that appear in the 2021 and 2022 datasets\n"
        "\n>**Covariates** are uncontrolled variables that may affect the outcome such as political party and religion.\n\n"
        
        "We get the following **results**\n"
        ">- **ATE** = 0.20\n"
        ">- **p-value** = 0.64\n\n"

        "Because p is greater than 0.05, **we don't have enough evidence to say events in 2022 affected opinions** " \
        "or that the null hypothesis is false. Therefore we fail to reject the null hypothesis. "
        ,unsafe_allow_html=True
    )
   
    
