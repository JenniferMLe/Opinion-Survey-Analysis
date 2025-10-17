import streamlit as st
import pandas as pd
import plotly.express as px
import utils
from scipy.stats import chi2_contingency

# read cleaned dataset from csv file
df_combined = pd.read_csv('Datasets/combined_dataset.csv')

# map filter choices to column names
demographics = ['Age','Race','Gender','Income','Marital Status',
                'Education','Party','Religion','Faith Importance','Pray Frequency']

# maps selection label to column names
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
    'Marital Status':'MARITAL',
    'Economy Rating':'ECON1MOD',
    'Economy Outlook in 1 Year':'ECON1BMOD'
}

# define order for categorical columns
category_orders = {
    'AGEGRP2':['18-24','25-39','40-59','60-79','80+'],
    'INCOMEGRP':['< $40K','$40-70K','$70-100K','$100K+'],
    'ECON1MOD':['Poor','Only fair','Good','Excellent'],
    'ECON1BMOD':['Better','About the same','Worse'],
    'PARTY':['Democrat','Republican','Independent','Other'],
    'RELIMP':['Not at all important','Not too important','Somewhat important','Very important'],
    'MARITAL':['Never married','Living with a partner','Married','Divorced','Widowed'],
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
    "Who We're Studying",
    'Changes Over Time',
    'Who is Affected',
    'Significant Influence'
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
    with filter1: dg1 = st.selectbox("Demographic 1",demographics,index=8)
    with filter2: dg2 = st.selectbox("Demographic 2",demographics,index=5)
    with filter3: weighted = st.selectbox("Using Weighted Data",[True,False],index=1)
    
    basic_graph,correlation_graph = st.columns([1,3])

    with basic_graph:
        df = utils.get_count(df_combined,[col[dg1]],weighted)
        df['Percent'] = (df['Count'] / df['Count'].sum()).round(4) * 100

        fig = px.bar(
            df, 
            x=col[dg1], 
            y='Percent',
            title= f'{dg1} Categories Share',
            text_auto='.2s', # put numbers in K format
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
            df['Percent'] = (df['Count'] / df.groupby(col[dg2])['Count'].transform('sum')).round(4) * 100

            if len(df) <= 30:barmode = 'group'
            else: barmode = 'stack'

            fig = px.bar(
                df, 
                x=col[dg2], 
                y='Percent',
                title= f'{dg1} Categories Share Among {dg2} Categories',
                text_auto='.2s', # put numbers in K format
                category_orders=category_orders,
                template='plotly_dark',
                color_discrete_sequence=colors,
                color=col[dg1],
                barmode=barmode
            )
            fig.update_xaxes(title=dg2)
            fig.update_layout(legend_title_text=dg1)
            st.plotly_chart(fig,key='4')

with problem_tab:
    st.subheader("Problem: Pessimism in 2022")

    color_map = {
        'Excellent':"#0daa00",
        'Good':'#8fdc32',
        'Only fair':'#ffc500',
        'Poor':'#f6492a',
        'Better':"#8fdc32",
        'About the same':'#ffc500',
        'Worse':'#f6492a'
    }

    # this function displays a cluster bar graph dispalying yearly changes in a column in the combined dataframe
    def graph_changes(column,weighted,title):
        df_change = utils.get_count(df_combined,['YEAR',column],weighted)
        df_change['Percent'] = (df_change['Count'] / df_change.groupby('YEAR')['Count'].transform('sum')).round(4) * 100
        utils.write_to_file(df_change)

        fig = px.line(
            df_change,
            x='YEAR',
            y='Percent',
            color=column,
            title=title,
            hover_data=['Count'],
            category_orders=category_orders,
            color_discrete_map=color_map
        )
        fig.update_xaxes(type='category',title_text='')
        fig.update_traces(line=dict(width=8))
        fig.update_layout(legend_title_text='')
        
        return fig
    
    description,graphs = st.columns([0.25,1])

    with description:
        st.markdown('<div class="border">'  
        "From 2021 to 2022 ...<br><br>"

        "The percent of <b>poor</b> and <b>only fair</b> economy ratings \
            <b>increaesd by 16.6 percentage points</b>, from 48.2% to 64.8%.<br><br>"

        "The percent of <b>worse</b> economy outlooks <b>increased by 16.6 percentage points</b>, \
            from 21.6% to 38.2%.<br><br>"
        
        "The percent of <b>better</b> economy outlooks <b>decreased by 13 percentage points</b>, \
            from 32.8% to 19.9%."

        '</div>', unsafe_allow_html=True)

    with graphs:
        weighted = st.selectbox("Using Weighted Data", [True,False])
        problem1,problem2 = st.columns([1,1])
        with problem1: st.plotly_chart(graph_changes('ECON1MOD',weighted,'Percentage of each Economy Rating by Year'))
        with problem2: st.plotly_chart(graph_changes('ECON1BMOD',weighted,'Percentage of each Economy Outlook by Year'))

with details_tab:
    st.subheader("Increase in Percentage of Respondants with Negative Sentiment from 2021 to 2022")

    filter1,filter2 = st.columns([1,1])
    with filter1: demographic = st.selectbox("Demographic", demographics, index=3)
    with filter2: weighted = st.selectbox("Using Weighted Data", [True,False],key=10)

    def graph_percent_increase(group,metric,weighted,title):
        if metric != 'Both':
            use = col[metric]
        else:
            use = 'Both'
        df = utils.get_percent_increase(df_combined,col[group],use,weighted)

        fig = px.bar(
            df,
            x=col[group],
            y='PercentNegDiff',
            title=title,
            color=df.columns[0],
            text_auto='.2s', # put numbers in K format
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
        fig = graph_percent_increase(demographic,'Economy Rating',weighted,
            'Metric: Economy Rating<br><sub>Increase in "poor" or "only fair" ratings</sub>')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    with graph2:
        fig = graph_percent_increase(demographic,'Economy Outlook in 1 Year',weighted,
            'Metric: Economy Outlook<br><sub>Increase in "worse" outlooks</sub>')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
    
    with graph3:
        fig = graph_percent_increase(demographic,'Both',weighted,
            'Metric: Both<br><sub>Increase in "worse" or "about the same" outlook with "poor" or "only fair" ratings')
        st.plotly_chart(fig)
    
with testing_tab:
    st.subheader('Do Certain Demographics Significantly Impact Negative Sentiment in 2022')

    filters,hypothesis = st.columns([1,4])
    with filters:
        group = st.selectbox("Test Group",demographics)
        metric = st.selectbox("Metric for Negative Sentiment",['Economy Rating','Economy Outlook in 1 Year','Both'])
        weighted = st.selectbox("Using Weighted Data",[True,False],key=9)
    
    df = df_combined[(df_combined['YEAR']== 2022)]
    if metric == 'Economy Rating':
        df_neg = df[df['ECON1MOD'].isin(['Poor','Only fair'])]
        df_pos = df[df['ECON1MOD'].isin(['Excellent','Good'])]
    elif metric == 'Economy Outlook in 1 Year':
        df_neg = df[df['ECON1BMOD'] == 'Worse']
        df_pos = df[df['ECON1BMOD'].isin(['About the same','Better'])]
    else:
        df_neg = df[(df['ECON1BMOD'] == 'Worse') | ((df['ECON1BMOD'] == 'About the same') & (df['ECON1MOD'].isin(['Poor','Only fair'])))]
        df_pos = df[(df['ECON1BMOD'] == 'Better') | ((df['ECON1BMOD'] == 'About the same') & (df['ECON1MOD'].isin(['Good','Excellent'])))]

    df_neg = utils.get_count(df_neg,[col[group]],weighted)
    df_pos = utils.get_count(df_pos,[col[group]],weighted)

    df = pd.DataFrame()
    df[col[group]] = df_neg[col[group]]
    df['CountNeg'] = df_neg['Count']
    df['CountPos'] = df_pos['Count']
    df['Share of Negative Sentiment (%)'] = round((df['CountNeg'] / (df['CountNeg'].sum())*100),2)
    total = df['CountNeg'].sum() + df['CountPos'].sum()
    df['Share of Total Responses (%)'] = round(((df['CountNeg'] + df['CountPos']) / total) * 100, 2)

    chi2, p, dof, expected = chi2_contingency(df[['CountNeg','CountPos']])
    if p < 0.05: s = ''
    else: s = 'don\'t'

    with hypothesis:
        st.markdown('<div class="border">'  
        
        "If there's no significant impact, each category's share of negative \
        sentiment should be about the same as its share of total responses. <br><br>"

        "For example, if 25% of responses to 'Economy Rating' have an income of <$40K, \
        25% of negative economy ratings should be from income = <$40K if income does \
        not impact negative sentiment. The table below compares the two shares. \
        We'll test for significance using a <b>chi-squared test</b>.<br><br>"
                    
        f"<b>Null Hypothesis</b>: {group} does not significantly impact negative sentiment \
        i.e {group} and negative sentiment are independent.<br>"

        f"<b>Alternative Hypothesis</b>: {group} significantly impacts negative sentiment \
        i.e {group} and negative sentiment are dependent.<br><br>"

        "<b>if p-value < 0.05 → reject the null hypothesis</b> \
            → the alternative hypothesis is more likely<br>"

       "<b>if p-value ≥ 0.05 → don't reject the null hypothesis</b> \
            → the null hypothesis is more likely<br><br>"

        f"<b>p-value = {round(p,2)} → {s} reject the null hypothesis"
        
        '</div>', unsafe_allow_html=True)
        
    st.dataframe(df[[col[group],'Share of Negative Sentiment (%)','Share of Total Responses (%)']])
    