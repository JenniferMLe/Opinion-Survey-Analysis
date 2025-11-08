import streamlit as st
from Tabs import tab1_intro, tab2_demographics, tab3_problem, tab4_details, tab5_correlation

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .border { 
            border-style: solid;
            border-color: #CCCCCC;
            background-color: #EDEDED;
            padding: 4px 4px 4px 4px;
            margin-bottom: 7px;
        }
    </style>
    """, unsafe_allow_html=True
)

# defining tabs
intro_tab,demographics_tab,problem_tab,details_tab,correlation_tab = st.tabs([
    'Intro',
    "Survey Participants",
    'Changes Over Time',
    'Driving Force',
    'Correlation'
])

with intro_tab:
    tab1_intro.show()

with demographics_tab:
    tab2_demographics.show()

with problem_tab:
    tab3_problem.show()

with details_tab:
    tab4_details.show()

with correlation_tab:
    tab5_correlation.show()