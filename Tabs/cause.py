import utils
import streamlit as st
import plotly.express as px

# create local constants from utils so we don't have to keep doing util.
df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    st.header("What cause an increase in negative economy ratings in 2022?")    
    st.markdown('<div class="border">'  
    "Events happening in 2021 and 2022 could have affected sentiment "
    "such as Joe Biden taking office and rising inflation rates. "

    "Inflation rates represent the increase in prices compared to the previous year. " 
    "At its peak, the 12-month inflation rate was 9.1% in June of 2022 meaning prices on average " 
    "were 9.1% more expensive compared to June of 2021. View inflation rate trends from 2000-current "
    '<a href="https://www.usinflationcalculator.com/inflation/current-inflation-rates/" target="_blank">here. </a><br><br>'

    "Let's see if the increase in negative sentiment was caused by inflation rates by holding " 
    " features than may affect it constant such as political affliation and age."
    '</div>', unsafe_allow_html=True)

    
    
