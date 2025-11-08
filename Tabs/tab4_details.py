import utils
import streamlit as st
import plotly.express as px

df_combined = utils.df_combined
demographics, social_media = utils.demographics, utils.social_media
col, category_orders, colors = utils.col, utils.category_orders, utils.colors

def show():
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
            fig = graph_percent_increase(demographic,'Economy Rating Category',weighted,
                'Metric 1: Economy Rating<br><sub>Increase in "poor" or "only fair" ratings</sub>')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

        with graph2:
            fig = graph_percent_increase(demographic,'Economy Outlook Category',weighted,
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
            "but the second lowest increase in economy outlook."
        '</div>', unsafe_allow_html=True)

    facet_graph = st.container()

    with facet_graph:
        st.subheader("Distribution of Economy Ratings and Outlooks Amoung Demographic Categories")
        
        filter1,filter2,filter3 = st.columns([1,1,1])
        
        with filter1: metric = st.selectbox("Metric", 
            ['Economy Rating','Economy Outlook','Economy Rating and Outlook','Economy Rating Category','Economy Outlook Category'])
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
