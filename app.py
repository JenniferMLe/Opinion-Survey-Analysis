import streamlit as st
from Tabs import intro, demographics, problem, causal_insights, sentiment_prediction

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
intro_tab,demographics_tab,problem_tab,causal_tab,prediction_tab = st.tabs([
    'Intro',
    "Survey Participants",
    'Changes Over Time',
    'Casual Insights',
    'Sentiment Prediction'
])

with intro_tab:
    intro.show()

with demographics_tab:
    demographics.show()

with problem_tab:
    problem.show()

with causal_tab:
    causal_insights.show()

with prediction_tab:
    sentiment_prediction.show()