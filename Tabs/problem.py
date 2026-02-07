import streamlit as st
import plotly.express as px
import utils 

# create local constants from utils so we don't have to keep doing util.
df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    st.subheader("Pessimism in 2022")

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
        'Neutral':'#ffc500'
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

    # create graph showing shares of demographic categories for each rating or outlook
    # e.g out of all poor econ ratings, what percent does <$40K contribute?
    facet_graph = st.container()

    with facet_graph:
        st.subheader("Distribution of Economy Ratings and Outlooks Among Demographic Categories")
        
        filter1,filter2,filter3 = st.columns([1,1,1])
        
        with filter1: metric = st.selectbox("Metric", 
            ['Economy Rating','Economy Outlook','Economy Rating and Outlook'])
        with filter2: dg = st.selectbox("Demographic",demographics,index=3)
        with filter3: weighted = st.selectbox("Use Weighted Data",[True,False])
       
        df = utils.get_count(df_combined,['Year',col[metric],col[dg]],weighted)
        df['share'] = round((df['count'] / df.groupby(['Year',col[metric]])['count'].transform('sum')) * 100,0).astype(int)
        df = df[df[col[metric]] != 'Refused']
        df = df[df[col[dg]] != 'Refused']

        fig = px.line(
            df,
            x='Year',
            y='share',
            color=col[dg],
            facet_col=col[metric],
            title=f'{dg} Categories Share by {metric} and Year',
            hover_data={
                col[metric]:False,
                'count':True,
                'share':True,
                'Year':False
            },
            labels = {
                'count':'n',
                'share':'share(%)',
            },
            category_orders=category_orders,
            color_discrete_sequence=colors
        )
        fig.update_xaxes(type='category',title_text='')
        fig.update_traces(line=dict(width=4))
        fig.update_layout(legend_title_text='')
        # make labels more readable by replacing column name 
        for annotation in fig.layout.annotations:
            if col[metric]+ "=" in annotation.text:
                annotation.text = annotation.text.replace(col[metric]+ "=", metric+" = ")

        st.plotly_chart(fig)

        st.markdown('<div class="border">'  
            "- In 2021, individuals making less than $40K made up 58% or poor ratings but that decreased to 40% "
            "in 2022 because of other income groups increasing their share.<br>"
            " - Shares of democrat and republican flip-flop after every election year (2020, 2024)"
        '</div>', unsafe_allow_html=True)

    increase_graphs = st.container()

    # create graphs displaying percentage point increase in the percent of 
    # each demographic category that have negative sentiment from 2021 to 2022
    # e.g if 60% <$40K have negative sentiment in 2021 and 70% in 2022, 
    # the percentage point increase is 10. 
    with increase_graphs:
        def graph_percent_increase(dg,metric,weighted,title):
            df = utils.get_percent_increase(df_combined,col[dg],col[metric],weighted)
            df = df[df[col[dg]]!='Refused']

            fig = px.bar(
                df,
                x=col[dg],
                y='percent_diff',
                title=title,
                color=df.columns[0],
                hover_data={
                    'percent_2021':True,
                    'percent_2022':True,
                    'n_2021':True,
                    'n_2022':True,
                    col[dg]:False
                },
                text_auto='.0f',
                category_orders=category_orders,
                color_discrete_sequence=colors
            )
            fig.update_xaxes(title=dg)
            fig.update_yaxes(title="Percentage Points Increase")
            fig.update_layout(legend_title_text=dg)
            
            return fig
        
        st.subheader("Increase in Percentage of Respondants with Negative Sentiment from 2021 to 2022")

        filter1,filter2 = st.columns([1,1])
        with filter1: dg = st.selectbox("Demographic", demographics+['Social Media'], index=3)
        with filter2: weighted = st.selectbox("Using Weighted Data", [True,False])

        graph1,graph2,graph3 = st.columns([1,1,1.25])
            
        with graph1:
            fig = graph_percent_increase(dg,'Economy Rating',weighted,
                'Metric 1: Economy Rating<br><sub>Increase in "poor" ratings</sub>')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

        with graph2:
            fig = graph_percent_increase(dg,'Economy Outlook',weighted,
                'Metric 2: Economy Outlook<br><sub>Increase in "worse" outlooks</sub>')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        
        with graph3:
            fig = graph_percent_increase(dg,'Economy Rating and Outlook',weighted,
                'Metric 3: Economy Rating and Outlook<br><sub>Increase in "worse" or "about the same" outlook with "poor" ratings')
            st.plotly_chart(fig)

        st.markdown('<div class="border">'  
            "- The <b>highest income group (>$100K)</b> have the greatest increase " \
            "in negative sentiment by metric 3.<br>"

            "- Individuals with a <b>Bachelor's Degree or higher</b> have the greatest increase in " \
            "negative sentiment by metric 2.<br>"

            "- <b>Non-religious individuals (faith importance = not too important)</b> have the lowest increase " \
            "in negative economy ratings but the greatest increase in negative economy outlook.<br>" 
            
            "- <b>LinkedIn users</b> have the highest increase in negative sentiment by metrics 2 and 3.<br>"

            "- <b>Republicans</b> have the highest increase in negative economy ratings " \
            "but the lowest increase in economy outlook."
        '</div>', unsafe_allow_html=True)