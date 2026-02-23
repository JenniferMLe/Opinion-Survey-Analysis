import streamlit as st

def show():
    st.subheader('Driving Forces of Negative Sentiment in 2022')
    shap_plot,description = st.columns([1.5,1])

    with shap_plot:
        st.markdown(
            """
            <style>
            img {
                height: 500px 
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.image("SHAP.png")
    
    with description:
        st.markdown(
        '<div class="border">'  
            "The graph to the left was created by <br><br>" \
            "1) using XGBoost to <b>predict if a person's overall sentiment will be negative</b> in 2022 <br><br>"
            "2) getting SHAP values which tells us <b>which features had the most impact on negative sentiment</b><br><br>"
            
            "The <b>features at the top</b> were the most impactful on predictions. <br><br>"

            "For <b>binary features</b> like 'Voted Joe Biden', a high feature value means the person voted for Joe Biden. " \
            "A low feature value means the person did not vote for Joe Biden. <br><br>"

            " Having a negative <b>SHAP value</b> means that the observation decreased the probability of having negative sentiment. " \
            "For example, not voting for Donald Trump in the 2020 election (blue dots) decreases the predicted probability " \
            "of having negative sentiment in 2022. "
        '</div>'
    ,unsafe_allow_html=True)

