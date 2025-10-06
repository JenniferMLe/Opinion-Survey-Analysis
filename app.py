import streamlit as st
import pandas as pd
import plotly.express as px
import utils

# read cleaned dataset from csv file
df_combined = pd.read_csv('Datasets/combined_dataset.csv')

# map filter choices to column names
demographics = ['Age','Race','Gender','Income','Education','Party','Religion','Faith Importance','Pray Frequency']
col = {
    'Age':'AGEGRP2',
    'Race':'RACE',
    'Gender':'GENDER',
    'Income':'INCOMEGRP',
    'Education':'EDUCATION',
    'Party':'PARTY',
    'Religion':'RELIG',
    'Faith Importance':'RELIMP',
    'Pray Frequency':'PRAY',
    'Economy Rating':'ECON1MOD',
    'Economy Outlook in 1 Year':'ECON1BMOD',
    'Use weighted data':True,
    'Use raw data':False
}

# define order for categorical columns
category_orders = {
    'AGEGRP2':['18-24','25-39','40-59','60-79','80+'],
    'INCOMEGRP':['< $40K','$40-70K','$70-100K','$100K+'],
    'ECON1MOD':['Poor','Only fair','Good','Excellent'],
    'ECON1BMOD':['Better','About the same','Worse'],
    'PARTY':['Democrat','Republican','Independent','Other'],
    'RELIMP':['Not at all important','Not too important','Somewhat important','Very important'],
    'EDUCATION':[
        "No schooling completed",
        "Some High School",
        "High School",
        "Some College",
        "Associate's Degree",
        "Bachelor's Degree",
        "Master's Degree or Higher"
    ],
    'PRAY':[
        'Never',
        'Seldom',
        'A few times a month',
        'Once a week',
        'A few times a week',
        'Once a day',
        'Several times a day'
    ]
}

# page setup
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
            border-color: #003f7eff;
            background-color: #C9EFFF;
            padding: 4px 4px 4px 4px;
            margin-bottom: 7px;
        }
    </style>
    """, unsafe_allow_html=True
)
# defining tabs
intro_tab,demographics_tab,problem_tab,details_tab,testing_tab,end_tab = st.tabs([
    'Intro',
    "Who We're Studying",
    'Changes Over Time',
    'Who is Affected',
    'Hypothesis Testing',
    'End'
])

with intro_tab:
    st.header("Opinion Survey Analysis")    
    st.markdown('<div class="border"></div>', unsafe_allow_html=True)
    
    st.write(
        '''
        In this analysis, using data from the National Public Opinion Reference surveys (NPORS) we will

        1. Examine how opinions on the economy has changed from 2020 to 2025 
        2. Examine which groups are most affected when opinions about the economy decline
        3. Examine if different things like income and education significantly impact negative or positive sentiment

        Below is the cleaned dataset used to conduct this study. 
        '''
    )
    st.markdown('<div class="border"></div>', unsafe_allow_html=True)
   
    st.dataframe(df_combined)

with demographics_tab:
    filter1,filter2,filter3 = st.columns([1,1,1])

    with filter1: dg1 = st.selectbox("Demographic 1",demographics,index=3)
    with filter2: dg2 = st.selectbox("Demographic 2",demographics,index=4)
    with filter3: weighted = st.selectbox("Using Weighted Data",[True,False],index=1)
    
    basic_graph,correlation_graph = st.columns([1,3])

    with basic_graph:
        if weighted: df = utils.get_count_weighted(df_combined,[col[dg1]])
        else: df = utils.get_count(df_combined,[col[dg1]])
        df['Percent'] = (df['Count'] / df['Count'].sum()).round(4) * 100

        fig = px.bar(
            df, 
            x=col[dg1], 
            y='Percent',
            title= 'Proportion of Each ' + dg1 + ' Category',
            text_auto='.2s', # put numbers in K format
            category_orders=category_orders,
            template='plotly_dark',
            color=col[dg1],
        )
        fig.update_xaxes(title=dg1).update_layout(showlegend=False)
        st.plotly_chart(fig,key='6')

    with correlation_graph:
        if weighted:df = utils.get_count_weighted(df_combined,[col[dg2],col[dg1]])
        else: df = utils.get_count(df_combined,[col[dg2],col[dg1]])
        df['Percent'] = (df['Count'] / df.groupby(col[dg2])['Count'].transform('sum')).round(4) * 100

        if len(df) <= 30:barmode = 'group'
        else: barmode = 'stack'

        fig = px.bar(
            df, 
            x=col[dg2], 
            y='Percent',
            title='Proportion of Each ' + dg1 + ' Category in Relation to Each ' + dg2 + ' Category',
            text_auto='.2s', # put numbers in K format
            category_orders=category_orders,
            template='plotly_dark',
            color=col[dg1],
            barmode=barmode
        )
        fig.update_xaxes(title=dg2)
        st.plotly_chart(fig,key='4')

# with problem_tab:
#     color_map = {
#     'Excellent':"#0daa00",
#     'Good':'#8fdc32',
#     'Only fair':'#ffc500',
#     'Poor':'#f6492a',
#     'Better':"#8fdc32",
#     'About the same':'#ffc500',
#     'Worse':'#f6492a'
#     }
#     # this function displays a cluster bar graph dispalying yearly changes in a column in the combined dataframe
#     def examine_changes(column,weighted,title):
#         if weighted:
#             df_change = utils.get_count_weighted(df_combined,['YEAR',column])
#         else:
#             df_change = utils.get_count(df_combined,['YEAR',column])
#         df_change['Percent'] = (df_change['Count'] / df_change.groupby('YEAR')['Count'].transform('sum')).round(4) * 100
#         utils.write_to_file(df_change)

#         fig = px.line(
#             df_change,
#             x='YEAR',
#             y='Percent',
#             color=column,
#             title=title,
#             hover_data=['Count'],
#             category_orders=category_orders,
#             color_discrete_map=color_map
#         )
#         fig.update_xaxes(type='category',title_text='')
#         fig.update_traces(line=dict(width=8))
#         fig.update_layout(legend_title_text='')
        
#         return fig

#     # weighted filter
#     weighted = st.selectbox("Choose weighted or raw data", ['Use weighted data','Use raw data'])
#     weighted = col[weighted]

#     problem1,problem2 = st.columns([1,1])
#     with problem1: st.plotly_chart(examine_changes('ECON1MOD',weighted,'Economy Rating'))
#     with problem2: st.plotly_chart(examine_changes('ECON1BMOD',weighted,'Economy Outlook in 1 Year'))

#     st.text_area("","Put description here.")

# with details_tab:
#     def graph_percent_increase(col,group_name):
#         df = utils.get_percent_increase(df_combined,col)

#         fig = px.bar(
#             df,
#             x='YEAR',
#             y='PercentNegDiff',
#             title='Difference in Negative Economy Ratings Percentages From Previous Year For ' + group_name + ' Groups',
#             barmode='group',
#             color=df.columns[0],
#             hover_data=['YEAR'],
#             category_orders=category_orders,
#             color_discrete_map=color_map
#         )
#         (fig
#             .update_yaxes(title="Difference")
#             .update_xaxes(type='category')
#             .update_layout(legend_title_text=group_name)
#         )
#         return fig

#     filter3,filter4 = st.columns([1,1])

#     with filter3:
#         demographic2 = st.selectbox("Choose a demographic", 
#                                     ['Age','Race','Gender','Income','Education','Party','Religion'],key='5')
        
#     col_name = col[demographic2]
        
#     st.plotly_chart(graph_percent_increase(col_name,demographic2))
#     st.text_area('','Enter Description for Detail Tab Here.')

# with end_tab:
#     st.title("Thank You For Viewing!")
    