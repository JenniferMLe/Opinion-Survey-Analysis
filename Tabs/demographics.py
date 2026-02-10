import utils
import streamlit as st
import pandas as pd
import plotly.express as px

# create local constants from utils so we don't have to keep doing util.
df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
    st.subheader("Demographics of Survey Participants")

    # create filters
    filter1,filter2,filter3 = st.columns([1,1,1])
    with filter1: dg1 = st.selectbox("Demographic 1",demographics,index=9)
    with filter2: dg2 = st.selectbox("Demographic 2",demographics,index=4)
    with filter3: weighted = st.selectbox("Using Weighted Data",[True,False],index=1)
    
    single_cat_graph, multi_cat_graph = st.columns([1,3])

    # creates and displays a graph of shares of demographic 1 categories
    with single_cat_graph:
        # get the count of each demographic1 value
        df = utils.get_count(df_combined,[col[dg1]],weighted)
        # get the share of each demographic1 category by dividing each category count with total count
        df['share'] = (df['count'] / df['count'].sum()).round(2) * 100
        # prevent refused demographic1 from showing on graph
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
                'text':'Share'
            },
            category_orders=category_orders,
            template='plotly_dark',
            color_discrete_sequence=colors,
            color=col[dg1],
        )
        fig.update_xaxes(title=dg1).update_layout(showlegend=False)
        st.plotly_chart(fig)
    
    # creates and displays a graph of shares of demographic 1 categories among demographic 2 categories
    with multi_cat_graph:
        if dg1 != dg2: 
            # get the count of each demographic1 and demographic2 value combo e.g <$40K and 'High School'
            df = utils.get_count(df_combined,[col[dg2],col[dg1]],weighted)
            # get the share of of each count by each demographic2
            df['share'] = (df['count'] / df.groupby(col[dg2])['count'].transform('sum')).round(2) * 100
            df = df[df[col[dg1]] != 'Refused']
            df = df[~df[col[dg2]].isin(['Other','Refused'])]

            # convert grouped bar to stacked bar graph is theres too many rows
            if len(df) <= 30:barmode = 'group'
            else: barmode = 'stack'

            fig = px.bar(
                df, 
                x=col[dg2], 
                y='share',
                title= f'{dg1} Categories Share Among {dg2} Categories',
                text = df['share'].astype(int).astype(str) + '%',
                hover_data={
                    'count':True,
                    'share':False,
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
            st.plotly_chart(fig)

    social_media_graph, weighted = st.columns([5,1])

    with weighted: 
        weighted = st.radio('',['Use weighted data', 'Use raw data'],horizontal=True,key=1)
        if weighted == 'Use weighted data': weighted = True
        else: weighted = False

    # create graph displaying social media usage
    with social_media_graph:
        social_media_df = pd.DataFrame()
        # for each social media column
        for sm in social_media:
            # get the count of each value ('Use','Don't Use', and 'Refuse')
            df = utils.get_count(df_combined,sm,weighted)
            # insert a column labeling which social media the counts are associated with
            df.insert(0, 'social_media', sm)
            # get the percent of percent of each value
            df['percent'] = round((df['count'] / df['count'].sum()) * 100,0).astype(int)
            # rename the column (name of social media) to usage so we can concat other
            # social media columns without duplicate columns for usage vals ('Use',etc.)
            df = df.rename(columns={sm:'Usage'})
            # concat to social_media_df
            social_media_df = pd.concat([df,social_media_df])

        # Only include rows where usage is 'Use'
        social_media_df = social_media_df[social_media_df['Usage'] == 'Yes']
        
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
        st.plotly_chart(fig)
    
    st.subheader('Summary Table')
    table,description = st.columns([2,1])

    # create summary table displaying 
    #   the raw and weighted count of each feature,
    #   the raw and weighted share of each feature
    with table:
        summary_table = pd.DataFrame()
        for feature in social_media + demographics[::-1]:
            # if we need to convert the feature to its column name
            if feature in col:
                feature = col[feature]
            
            # get unweighted count and share
            df = utils.get_count(df_combined,feature,False)
            df['percent'] = df['percent'] = (df['count'] / df['count'].sum()).round(2) * 100
            df = df.rename(columns={feature:'group'})
            df.insert(0, 'demographic', feature)

            # get the weighted count and share
            df_weighted = utils.get_count(df_combined,feature,True)
            df_weighted['percent'] = df_weighted['percent'] = (df_weighted['count'] / df_weighted['count'].sum()).round(2) * 100
            
            # added weighted count and share to df
            df['weighted_count'] = df_weighted['count']
            df['weighted_percentage'] = df_weighted['percent']

            # concat counts and share of this feature to all features df
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