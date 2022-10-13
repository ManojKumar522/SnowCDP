#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import required libraries

from snowflake.snowpark.session import Session
import streamlit as st
import pandas as pd
from Config import connection_parameters as CP
import plotly.express as px
import streamlit.components.v1 as components


# In[2]:


# Create Session object
def create_session_object():
    connection_parameters = CP
    
    session = Session.builder.configs(connection_parameters).create()
    print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())
    return session



# In[3]:


# Fetching the Data from tables to DF.
snow_df_rfm = create_session_object().table('RFM_RESULTS')


# In[4]:


# Convert Snowpark DataFrames to Pandas DataFrames for Streamlit
pd_df_rfm = snow_df_rfm.to_pandas()


# In[5]:

st.set_page_config(layout="wide")

header = st.container()
charts = st.container()
dataset = st.container()



with header:
    st.title("Demo Title")    
    
    
with charts:
    st.header("CHARTS")
    col1, col2,col3 = st.columns(3)
    pie_df_label_count = pd_df_rfm.groupby(['LABEL'], as_index=False)[['CUSTOMERID','RECENCY']].count()
    pie_df_label_monetary_sum = pd_df_rfm.groupby(['LABEL'], as_index=False)['MONETARY'].sum()
    
    
    col3.subheader("Pie2")
    pie_1 = px.pie(pie_df_label_count, values = 'CUSTOMERID', names='LABEL', color='LABEL',
             color_discrete_map={'Gold':'#D1B000',
                                 'Silver':'gray',
                                 'Bronze':'#CD7F32'})
                   
    pie_1.update_layout(
                    autosize=False,
                    width=400,
                    height=400,
                    margin=dict(
                        l=100,
                        r=50,
                        b=100,
                        t=50,
                        pad=4
                    ), paper_bgcolor="#D3D3D3",
)


    col3.write(pie_1)
    

    col2.subheader("Pie1")
    pie_2 = px.pie(pie_df_label_monetary_sum, values = 'MONETARY', names='LABEL', hole = 0.65, color='LABEL',
             color_discrete_map={'Gold':'#D1B000',
                                 'Silver':'gray',
                                 'Bronze':'#CD7F32'})

    pie_2.update_layout(
                    autosize=False,
                    width=400,
                    height=400,
                    margin=dict(
                        l=50,
                        r=100,
                        b=100,
                        t=50,
                        pad=4
                    )
)
    col2.write(pie_2)
    
    col1.subheader("Lifestage")
    pd_df_lifestage_agg = pd_df_rfm.groupby(['LIFESTAGE','LABEL'], as_index=False)['CUSTOMERID'].count()
    pd_df_lifestage_agg = pd_df_lifestage_agg.pivot(index='LIFESTAGE', columns='LABEL', values='CUSTOMERID',)
    # col1.write(pd_df_lifestage_agg)
    col1.dataframe(pd_df_lifestage_agg, width=400)
        
    
    # app = Dash(__name__)
    
    # app.layout = dash_table.DataTable(
    # data=pd_df_lifestage_agg,
    # sort_action='native',
    # columns=[
    #     {'name': 'Gold', 'id': 'Gold', 'type': 'Float',},
    #     {'name': 'Silver', 'id': 'Silver', 'type': 'Float',},
    #     {'name': 'Bronze', 'id': 'Bronze', 'type': 'Float',},
    # ],
    # editable=True,
    # style_data_conditional=[
    # {
    #     'if': {
    #         'column_id': 'Gold',
    #         },
    #     'backgroundColor': 'dodgerblue',
    #     'color': 'white'
    # },])

    # if __name__ == '__main__':
    #     app.run_server(debug=True)

    
    
    
with dataset:
    pie_col = st.columns(1)
    st.header("Customer List")
    st.write(pd_df_rfm.head(20))
    
    
    
components.html(
    """
    <div id="accordion">
        <h1>"Hello"</h1>
    </div>
    """
)

    
