import utils 
import streamlit as st

def show():
    st.header("Opinion Survey Analysis")    
    st.markdown('<div class="border">'  
    "In this analysis using data from NPORS - National Public Opinion Reference surveys (more info "
    '<a href="https://www.pewresearch.org/methods/fact-sheet/national-public-opinion-reference-survey-npors/" target="_blank">here</a>), we will <br><br>' 

    "&nbsp;&nbsp;&nbsp;&nbsp;1. Examine how opinions on the economy have changed from 2020 to 2025<br>"
    "&nbsp;&nbsp;&nbsp;&nbsp;2. Discover driving forces when opinions about the economy become more pessimistic<br>"
    "&nbsp;&nbsp;&nbsp;&nbsp;3. Test if economic events caused changes in sentiment<br><br>"

    "Below is the cleaned dataset used to conduct this study."
    '</div>', unsafe_allow_html=True)

    st.dataframe(utils.df_combined)