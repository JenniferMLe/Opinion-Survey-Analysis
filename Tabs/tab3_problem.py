import streamlit as st
import plotly.express as px
import utils 

# create local constants from utils so we don't have to keep doing util.
df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    st.subheader("Problem: Pessimism in 2022")

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
        'Positive':"#0daa00"
    }
    
    graphs = st.container()

    with graphs:
        # displays line graph showing changes in opinions about the economy
        # metric is economy rating, economy outlook, etc.
        def graph_changes(metric,weighted,title):
            # get count of each year and metric values combination e.g 2020 and 'Only Fair'
            df = utils.get_count(df_combined,['Year',metric],weighted)
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
        with problem3: st.plotly_chart(graph_changes('Econ_Rating_Outlook',weighted,'Share of Negative Sentiment by Year'))

    description = st.container()

    with description:
        st.markdown('<div class="border">'  
        '*Sentiment is negative when outlook = "worse" or when outlook = "about the same" and rating = "poor" or "only fair".<br><br>'
        "From 2021 to 2022 ...<br>"

        "- The percent of <b>poor</b> and <b>only fair</b> economy ratings \
            <b>increaesd by 16.6 percentage points</b>, from 48.2% to 64.8%.<br>"

        "- The percent of <b>worse</b> economy outlooks <b>increased by 16.6 percentage points</b>, \
            from 21.6% to 38.2%.<br>"
        
        "- The percent of <b>better</b> economy outlooks <b>decreased by 13 percentage points</b>, \
            from 32.8% to 19.9%."

        '</div>', unsafe_allow_html=True)