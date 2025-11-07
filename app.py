import streamlit as st
import pandas as pd
import plotly.express as px
import utils 
import numpy as np
from scipy.stats import chi2_contingency
import math 

# read cleaned dataset from csv file
df_combined = pd.read_csv('Datasets/combined_dataset.csv')

# map filter choices to column names
demographics = ['Age','Race','Gender','Income','Education','Region','Party',
                'Marital Status','Religion','Faith Importance','Pray Frequency']

# maps selection label to column names
col = {
    'Age':'Age_Cat',
    'Race':'Race',
    'Gender':'Gender',
    'Income':'Income_Cat',
    'Region':'Region',
    'Education':'Education',
    'Social Media':'social_media',
    'Party':'Party',
    'Religion':'Religion',
    'Faith Importance':'Faith_Importance',
    'Pray Frequency':'Pray_Freq',
    'Marital Status':'Marital',
    'Economy Rating':'Econ_Rating',
    'Economy Rating Cat':'Econ_Rating_Cat',
    'Economy Outlook':'Econ_Outlook',
    'Economy Outlook Cat': 'Econ_Outlook_Cat',
    'Economy Rating and Outlook':'Econ_Rating_Outlook'
}

# define order for categorical columns
category_orders = {
    'Age_Cat':['18-24','25-39','40-59','60-79','80+'],
    'Income_Cat':['< $40K','$40-70K','$70-100K','$100K+'],
    'Econ_Rating':['Poor','Only Fair','Good','Excellent'],
    'Econ_Outlook':['Worse','About the same','Better'],
    'Party':['Democrat','Republican','Independent','Other'],
    'Faith_Importance':['Not at all important','Not too important','Somewhat important','Very important'],
    'Marital':['Never married','Living with a partner','Married','Divorced','Widowed'],
    'Education':[
        "No schooling completed",
        "Some High School",
        "High School",
        "Some College",
        "Associate's Degree",
        "Bachelor's Degree",
        "Master's Degree or Higher"
    ],
    'Pray_Freq':[
        'Never',
        'Seldom',
        'A few times a month',
        'Once a week',
        'A few times a week',
        'Once a day',
        'Several times a day'
    ]
}

# define graph colors
colors = [
    "#264653", "#2A9D8F", "#E9C46A",
    "#F4A261", "#E76F51", "#D3D3D3", "#1D3557"
]

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
intro_tab,demographics_tab,problem_tab,details_tab,testing_tab = st.tabs([
    'Intro',
    "Survey Participants",
    'Changes Over Time',
    'Driving Force',
    'Correlation and Casuation'
])

with intro_tab:
    st.header("Opinion Survey Analysis")    
    st.markdown('<div class="border">'  
    "In this analysis using data from NPORS - National Public Opinion Reference surveys (more info "
    '<a href="https://www.pewresearch.org/methods/fact-sheet/national-public-opinion-reference-survey-npors/" target="_blank">here</a>), we will <br><br>' 

    "&nbsp;&nbsp;&nbsp;&nbsp;1. Examine how opinions on the economy have changed from 2020 to 2025<br>"
    "&nbsp;&nbsp;&nbsp;&nbsp;2. Examine which groups are most affected when opinions about the economy become more pessimistic<br>"
    "&nbsp;&nbsp;&nbsp;&nbsp;3. Examine if different things like income and education significantly impact negative sentiment<br><br>"

    "Below is the cleaned dataset used to conduct this study."
    '</div>', unsafe_allow_html=True)
   
    st.dataframe(df_combined)

with demographics_tab:
    st.subheader("Demographics of Survey Participants")

    filter1,filter2,filter3 = st.columns([1,1,1])
    with filter1: dg1 = st.selectbox("Demographic 1",demographics,index=9)
    with filter2: dg2 = st.selectbox("Demographic 2",demographics,index=4)
    with filter3: weighted = st.selectbox("Using Weighted Data",[True,False],index=1)
    
    basic_graph,correlation_graph = st.columns([1,3])

    with basic_graph:
        df = utils.get_count(df_combined,[col[dg1]],weighted)
        df['share'] = (df['count'] / df['count'].sum()).round(2) * 100
        df = df[df[col[dg1]] != 'Refused']

        fig = px.bar(
            df, 
            x=col[dg1], 
            y='share',
            title= f'{dg1} Categories Share',
            text = df['share'].astype(int).astype(str) + '%',
            hover_data={
                'count':True,
                'share':False,
                col[dg1]:False
            },
            labels={
                'count':'n',
                'text':'share'
            },
            category_orders=category_orders,
            template='plotly_dark',
            color_discrete_sequence=colors,
            color=col[dg1],
        )
        fig.update_xaxes(title=dg1).update_layout(showlegend=False)
        st.plotly_chart(fig,key='6')

    with correlation_graph:
        if dg1 != dg2: 
            df = utils.get_count(df_combined,[col[dg2],col[dg1]],weighted)
            df['percent'] = (df['count'] / df.groupby(col[dg2])['count'].transform('sum')).round(2) * 100
            df = df[df[col[dg1]] != 'Refused']
            df = df[df[col[dg2]] != 'Refused']

            if len(df) <= 30:barmode = 'group'
            else: barmode = 'stack'

            fig = px.bar(
                df, 
                x=col[dg2], 
                y='percent',
                title= f'{dg1} Categories Share Among {dg2} Categories',
                text = df['percent'].astype(int).astype(str) + '%',
                hover_data={
                    'count':True,
                    'percent':False,
                    col[dg1]:False,
                    col[dg2]:False
                },
                labels={
                    'count':'n',
                    'text':'share'
                },
                category_orders=category_orders,
                template='plotly_dark',
                color_discrete_sequence=colors,
                color=col[dg1],
                barmode=barmode
            )
            fig.update_xaxes(title=dg2)
            fig.update_layout(legend_title_text=dg1)
            st.plotly_chart(fig,key='4')

    social_media_graph = st.container()

    with social_media_graph:
        sm = ['Facebook', 'Youtube', 'Twitter', 'Instagram', 'Snapchat',
            'Whatsapp', 'Linkedin', 'Pinterest', 'Tiktok', 'Bereal', 'Reddit']

        social_media_df = pd.DataFrame()
        for s in sm:
            df = utils.get_count(df_combined,s,weighted)
            df.insert(0, 'social_media', s)
            df['percent'] = round((df['count'] / df['count'].sum()) * 100,0).astype(int)
            df = df.rename(columns={s:'Usage'})
            social_media_df = pd.concat([df,social_media_df])

        social_media_df = social_media_df[social_media_df['Usage'] == 'Use']
        
        fig = px.bar(
            social_media_df, 
            x='social_media', 
            y='percent',
            title= 'Percent of Respondents Who Use Social Media (Among Those Surveyed)',
            text = social_media_df['percent'].astype(int).astype(str) + '%',
            hover_data={
                'social_media':False,
                'count':True,
                'percent':False,
            },
            labels = {
                'count':'n',
                'text':'usage'
            },
            template='plotly_dark',
            color_discrete_sequence=colors,
            color='social_media'
        )
        fig.update_xaxes(title='')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,key='99')
    
    st.subheader('Summary Table')
    table,description = st.columns([2,1])

    with table:
        summary_table = pd.DataFrame()
        for dg in sm + demographics[::-1]:
            if dg in col:
                dg = col[dg]
            df = utils.get_count(df_combined,dg,False)
            df['percent'] = df['percent'] = (df['count'] / df['count'].sum()).round(2) * 100
            df = df.rename(columns={dg:'group'})
            df.insert(0, 'demographic', dg)

            df_weighted = utils.get_count(df_combined,dg,True)
            df_weighted['percent'] = df_weighted['percent'] = (df_weighted['count'] / df_weighted['count'].sum()).round(2) * 100

            df['weighted_count'] = df_weighted['count']
            df['weighted_percentage'] = df_weighted['percent']
            summary_table = pd.concat([df,summary_table])
        
        st.dataframe(summary_table)
    
    with description:
        st.markdown('<div class="border">'  
        "<b>Age</b>: 68% between the ages of 40 and 79<br><br>"
        "<b>Race</b>: 74% white<br><br>"
        "<b>Income</b>: 58% make under $40,000 or above $100,000<br><br>"
        "<b>Education</b>: 55% have a college degree<br><br>"
        "<b>Religion</b>: 65% are Christians (Catholic or Protestant)<br>"
        '</div>', unsafe_allow_html=True)

with problem_tab:
    st.subheader("Problem: Pessimism in 2022")

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
        # this function displays a cluster bar graph dispalying yearly changes in a column in the combined dataframe
        def graph_changes(column,weighted,title):
            df = utils.get_count(df_combined,['Year',column],weighted)
            df['share'] = round((df['count'] / df.groupby('Year')['count'].transform('sum')) * 100,0).astype(int)
            df = df[df[column] != 'Refused']

            fig = px.line(
                df,
                x='Year',
                y='share',
                color=column,
                title=title,
                hover_data={
                    column:False,
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
        
        weighted = st.selectbox("Using Weighted Data", [True,False])
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

with details_tab:

    increase_graphs = st.container()

    with increase_graphs:
        st.subheader("Increase in Percentage of Respondants with Negative Sentiment from 2021 to 2022")

        filter1,filter2 = st.columns([1,1])
        with filter1: demographic = st.selectbox("Demographic", demographics+['Social Media'], index=3)
        with filter2: weighted = st.selectbox("Using Weighted Data", [True,False],key=10)

        def graph_percent_increase(group,metric,weighted,title):
            df = utils.get_percent_increase(df_combined,col[group],col[metric],weighted)
            df = df[df[col[group]]!='Refused']

            fig = px.bar(
                df,
                x=col[group],
                y='percent_diff',
                title=title,
                color=df.columns[0],
                hover_data={
                    'percent_2021':True,
                    'percent_2022':True,
                    'n_2021':True,
                    'n_2022':True,
                    col[group]:False
                },
                text_auto='.0f',
                category_orders=category_orders,
                color_discrete_sequence=colors
            )
            (fig
                .update_xaxes(title=group)
                .update_yaxes(title="Percentage Points Increase")
                .update_layout(legend_title_text=group)
            )
            return fig
        
        graph1,graph2,graph3 = st.columns([1,1,1.25])
            
        with graph1:
            fig = graph_percent_increase(demographic,'Economy Rating Cat',weighted,
                'Metric 1: Economy Rating<br><sub>Increase in "poor" or "only fair" ratings</sub>')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

        with graph2:
            fig = graph_percent_increase(demographic,'Economy Outlook Cat',weighted,
                'Metric 2: Economy Outlook<br><sub>Increase in "worse" outlooks</sub>')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        
        with graph3:
            fig = graph_percent_increase(demographic,'Economy Rating and Outlook',weighted,
                'Metric 3: Economy Rating and Outlook<br><sub>Increase in "worse" or "about the same" outlook with "poor" or "only fair" ratings')
            st.plotly_chart(fig)

        st.markdown('<div class="border">'  
            "- The <b>highest income group (>$70K)</b> have the greatest increase " \
            "in negative sentiment by metric 3.<br>"

            "- Individuals with a <b>Bachelor's Degree or higher</b> have the greatest increase in " \
            "negative sentiment by metric 2 and 3.<br>"

            "- <b>Religious individuals (faith importance = very important)</b> have the greatest increase " \
            "in negative economy ratings but the lowest increase in negative economy outlook.<br>" 
            
            "- <b>LinkedIn users</b> have the highest increase in negative sentiment by all 3 metrics.<br>"

            "- <b>Republicans</b> have the highest increase in negative economy ratings " \
            "but the lowest increase in economy outlook."
        '</div>', unsafe_allow_html=True)

    facet_graph = st.container()

    with facet_graph:
        st.subheader("Distribution of Economy Ratings and Outlooks Amoung Demographic Categories")
        
        filter1,filter2,filter3 = st.columns([1,1,1])
        
        with filter1: metric = st.selectbox("Metric", ['Economy Rating','Economy Outlook','Economy Rating and Outlook'])
        with filter2: dg = st.selectbox("Demographic",demographics,index=3,key=19)
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
        for annotation in fig.layout.annotations:
            if col[metric]+ "=" in annotation.text:
                annotation.text = annotation.text.replace(col[metric]+ "=", metric+" = ")

        st.plotly_chart(fig)

        # st.markdown('<div class="border">'  
        #     "- The <b>highest income group (>$70K)</b> have the greatest increase " \
        #     "in negative sentiment by metric 3.<br>"
        # '</div>', unsafe_allow_html=True)

with testing_tab:
    correlation = st.container()

    with correlation:
        filter1,filter2,blank = st.columns([1,1,2]) 
        with filter1: year = st.slider('year',2020,2025,value=2022)
        with filter2: weighted = st.radio('',['Use weighted data', 'Use raw data'])
        df = df_combined[df_combined['Year']==year]

        sm = ['Facebook', 'Youtube', 'Twitter', 'Instagram', 'Snapchat',
            'Whatsapp', 'Linkedin', 'Pinterest', 'Tiktok', 'Bereal', 'Reddit']
        
        metrics = ['Econ_Rating','Econ_Rating_Cat','Econ_Outlook','Econ_Outlook_Cat','Econ_Rating_Outlook']
        all_cors = []
        for metric in metrics:
            cors = []
            for feature in demographics + sm:
                if feature in col:
                    feature = col[feature]
                ct = df
                ct = ct[ct[metric] != 'Refused']
                ct = ct[ct[feature] != 'Refused']

                if weighted == 'Use weighted data':
                    ct = pd.crosstab(ct[feature], ct[metric], values=ct['Weight'], aggfunc='sum')
                else:
                    ct = pd.crosstab(ct[feature], ct[metric])

                if ct.size == 0:
                    cors.append(None)
                    continue

                ct = ct.fillna(0)
                chi2, p, dof, expected = chi2_contingency(ct)

                n = 0
                for c in ct.columns:
                    n += ct[c].sum()

                k = min(len(ct),len(ct.columns))
                cors.append(round(math.sqrt(chi2/(n*(k-1))),2))

            all_cors.append(cors)

            utils.write_to_file(pd.DataFrame(all_cors))

        data = pd.DataFrame(all_cors,index=metrics,columns=demographics+sm)

        fig = px.imshow(data, text_auto=True, title='Correlation Strength (0 to 1) Using Cramer\'s V')

        st.plotly_chart(fig)


        st.markdown('<div class="border">'  
            "- <b>Correlation</b> is the <b>association or dependence</b> between two variables.<br>" 
            "- We'll use <b>Cramer's V</b> to measure correlation since NPORS data is nominal "
            "(categories instead of numbers) and ordinal (categories with rank).<br>"
            "- Cramer's V <b>ranges from 0 to 1</b> with 0 being no dependence and 1 being complete dependence.<br>"
            "- <b>Guideline</b>: ≤ 0.2: weak association, 0.2 < X ≤ 0.6: moderate association, > 0.6: strong assocation"
            ""
        '</div>', unsafe_allow_html=True)
