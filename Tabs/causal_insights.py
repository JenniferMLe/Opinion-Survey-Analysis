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
    "Many events happened in 2021 and 2022 that could have affected sentiment in 2022 "
    "such as Joe Biden taking office in January of 2021 and rising inflation rates in 2022.<br>"
    "View inflation rate trends from 2000-current "
    '<a href="https://www.usinflationcalculator.com/inflation/current-inflation-rates/" target="_blank">here</a><br><br>'
    "Let's see if the increase in negative sentiment was caused by inflation rates by holding " 
    " features than may affect it constant such as political affliation and age."
    '</div>', unsafe_allow_html=True)

