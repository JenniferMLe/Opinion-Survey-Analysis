import utils
import streamlit as st
import pandas as pd
import plotly.express as px

df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
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
        social_media_df = pd.DataFrame()
        for s in social_media:
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
        for dg in social_media + demographics[::-1]:
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