import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import time
import numpy as np

st.set_page_config(
    page_title="Water Consumption in Malaysia",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.title("💧Water Consumption in Malaysia")

df=pd.read_csv('Water_Usage.csv')

#with st.sidebar:
#    st.title('💧Water Consumption in Malaysia')
#    year_list = list(df.Date.unique())[::-1]
#    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
#    df_selected_year = df[df.Date == selected_year]
#    df_selected_year_sorted = df_selected_year.sort_values(by="Water Consumed", ascending=False)

#    color_theme_list = ['blues', 'cividis', 'green', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
#    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

#create the column
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(
    label="# Total Water Used",
    value=f"{df['Water Consumed'].sum():,.0f}")
kpi2.metric(
    label="# Average per Year",
    value=f"{df['Water Consumed'].mean():,.0f}")
kpi3.metric(
    label="# Max Consumption",
    value=f"{df['Water Consumed'].max():,.0f}")

#create column for chart
fig_col1, fig_col2, fig_col3 = st.columns(3)
with fig_col1:
    st.markdown("# Malaysia Water Consumption Over Year")
    dfMAS=df[df['State']=='Malaysia'] #filter
    grouped=dfMAS.groupby(['Date','Sector'])['Water Consumed'].sum().unstack()
    grouped['Total']=grouped['Domestic']+grouped['Non-Domestic']
    grouped=grouped.reset_index()
    fig = px.line(
        grouped,
        x='Date',
        y='Total',
        labels={'Date': 'Year', 'Total': 'Water Consumption (MLD)'},
        markers=True
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with fig_col2:
    st.markdown("# Total Water Consumption by State in Malaysia")
    df_states_only = df[df['State'] != 'Malaysia']
    state_consumption = df_states_only.groupby('State', as_index=False)['Water Consumed'].sum()
    state_consumption = state_consumption.sort_values(by='Water Consumed', ascending=False)
    fig = px.bar(
        state_consumption,
        x='State',
        y='Water Consumed',
        labels={'Water Consumed': 'Total Water Consumed (MLD)'},
        color_discrete_sequence=['skyblue']
        )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

with fig_col3:
    st.markdown("# Domestic vs Non-Domestic Over Year")
    grouped_df = df.groupby(['Date', 'Sector'])['Water Consumed'].sum().reset_index()
    fig = px.line(
        grouped_df,
        x='Date',
        y='Water Consumed',
        color='Sector',
        markers=True,
        labels={
            'Date': 'Year',
            'Water Consumed': 'Water Consumed (MLD)',
            'Sector': 'Sector'
            },
        color_discrete_map={
            'Domestic': 'blue',
            'Non-Domestic': 'orange'
            }
        )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

st.markdown("### Detailed Data View")
st.dataframe(df)
time.sleep(1)