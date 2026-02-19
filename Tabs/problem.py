import streamlit as st
import plotly.express as px
from utils import get_count,df_combined,category_orders

def show():
    st.subheader("Problem: Opinions become more negative in 2022")

    # maps econ_rating and econ_outlook values to a color
    color_map = {
        'Excellent':"#0daa00",
        'Good':'#8fdc32',
        'Only Fair':'#ffc500',
        'Poor':'#f6492a',
        'Better':"#8fdc32",
        'About the same':'#ffc500',
        'Worse':'#f6492a',
        'Negative':'#f6492a',
        'Positive':"#0daa00",
        'Neutral':'#ffc500',
        'Mix': '#DEDEDE'
    }
    
    graphs = st.container()

    with graphs:
        # displays line graph showing changes in opinions about the economy
        # metric is economy rating, economy outlook, etc.
        def graph_changes(metric,weighted,title):
            # get count of each year and metric values combination e.g 2020 and 'Only Fair'
            df = get_count(df_combined,['Year',metric],weighted)
            # get the share of each metric value by year
            df['share'] = round((df['count'] / df.groupby('Year')['count'].transform('sum')) * 100,0).astype(int)
            df = df[df[metric] != 'Refused']

            fig = px.line(
                df,
                x='Year',
                y='share',
                color=metric,
                title=title,
                hover_data={
                    metric:False,
                    'count':True,
                    'share':True
                },
                labels = {
                    'count':'n',
                    'share':'Share(%)',
                },
                category_orders=category_orders,
                color_discrete_map=color_map
            )
            fig.update_xaxes(type='category',title_text='')
            fig.update_yaxes(range=[0, None])
            fig.update_traces(line=dict(width=6))
            fig.update_layout(legend_title_text='')
            
            return fig
        
        weighted = st.radio('',['Use weighted data', 'Use raw data'],horizontal=True,key=2)
        if weighted == 'Use weighted data': weighted = True
        else: weighted = False
        
        problem1,problem2,problem3 = st.columns([1,1,1])
        with problem1: st.plotly_chart(graph_changes('Econ_Rating',weighted,'Share of Economy Ratings by Year'))
        with problem2: st.plotly_chart(graph_changes('Econ_Outlook',weighted,'Share of Economy Outlooks by Year'))
        with problem3: st.plotly_chart(graph_changes('Econ_Sentiment',weighted,'Share of Overall Sentiment by Year'))

    sentiment_definition,oberservations = st.columns([1,1])    

    with sentiment_definition:
        st.markdown('<div class="border">'  
        '<b>Overall Sentiment</b> is ...<br>'
        '- <b>negative</b> when rating is "poor" & outlook is "worse" or "about the same"<br>'
        '- <b>negative</b> when rating is "only fair" & outlook is "worse"<br>'
        '- <b>neutral</b>  when rating is "only fair" & outlook is "about the same"<br>'
        '- <b>positive</b> when rating is "excellent" or "good" & outlook is "better" or "about the same"<br>'
        '- <b>mixed</b> when rating is postive but outlook is negative or vice versa'
        '</div>', unsafe_allow_html=True)

    with oberservations:
        st.markdown('<div class="border">'  
        "From 2021 to 2022 ...<br>"

        "- <b>Positive sentiment decreased</b> by 19 percentage points<br>"

        "- <b>Negative sentiment increased</b> by 17 percentage points"

        '</div>', unsafe_allow_html=True)

    