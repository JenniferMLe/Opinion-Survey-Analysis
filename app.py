import streamlit as st
from Tabs import intro, demographics, problem, cause, details

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
intro_tab,demographics_tab,problem_tab,details_tab,causal_tab = st.tabs([
    'Intro',
    'Who We\'re Studying',
    'Problem',
    'Deep Dive',
    'Cause'
])

with intro_tab:
    intro.show()

with demographics_tab:
    demographics.show()

with problem_tab:
    problem.show()

with causal_tab:
    cause.show()

with details_tab:
    details.show()



