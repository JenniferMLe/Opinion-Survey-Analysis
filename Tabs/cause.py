import utils
import streamlit as st
import plotly.express as px

# create local constants from utils so we don't have to keep doing util.
df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    st.header("What cause the problem?")    
    st.markdown('<div class="border">'  
    "<b>Events happening in 2021 and 2022 could have affected sentiment</b> "
    "such as Joe Biden taking office and rising inflation rates.<br><br> "

    "<b>Inflation rates</b> represent the increase in prices compared to the previous year. " 
    "At its peak, the 12-month inflation rate was 9.1% in June of 2022 meaning prices on average " 
    "were 9.1% more expensive compared to June of 2021. View inflation rate trends from 2000-current "
    '<a href="https://www.usinflationcalculator.com/inflation/current-inflation-rates/" target="_blank">here. </a><br><br>'

    "Let's see if the increase in negative sentiment was caused by economic events in 2022 such as rising " 
    "inflation rates by holding features than may affect it constant such as political affliation and age."
    '</div>', unsafe_allow_html=True)

    st.markdown(
        "\nUsing **causal inference**, doubly-robust correction, and the following set-up ... \n"  
        "> - **Control** → Year = 2021\n"
        "> - **Treatment** → Year = 2022\n"
        "> - **Outcome** → Overall Sentiment = 'Negative'\n"
        "> - **Covariates** → variables that appear in the 2021 and 2022 datasets\n\n"

        "We get an **average treatment effect** (ATE) of **0.21**. "
        "This means if everyone was from 2022, the probability of having negative "
        "sentiment would increase on average by 21 percentage points compared to if everyone was from 2021.\n\n"

        "**Covariates** are uncontrolled variables that may affect the outcome. "
        "For example if more republicans, religious people, or older adults happen to be selected for the 2022 study "
        "(when Joe Biden was president), we can't reliably say econmic events of 2022 "
        "caused the increase in negative sentiment because of selection bias.\n\n"
        
        "Using double robust corrections, we can account for possible selection biases. ",
        unsafe_allow_html=True
    )
   
    
