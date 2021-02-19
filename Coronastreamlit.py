
import pandas as pd
import numpy as np
import streamlit as st
import plotly
import plotly.graph_objects as go
import plotly.express as px
import scipy
import statsmodels.api

# load data
st.write("Statistics and Research")
st.title("Coronavirus Pandemic (COVID-19)")

st.subheader("Explore the global situation")
df = pd.read_csv(r'C:\Users\User\Desktop\MSBA-325 Fouad Zablith\session 2\corona\worldometer_coronavirus_summary_data.csv')

expander = st.beta_expander("Overview")
expander.write("Statistics on the coronavirus pandemic showing total confirmed cases, total deaths, total recovered, active cases, total tests and population for every country in the world until 12 of February 2021.")

if st.checkbox("Show data"):
    st.write("Data until 12 of February 2021")
    df


#Draw map
#another source of data
df2 = pd.read_csv(r'C:\Users\User\Desktop\MSBA-325 Fouad Zablith\session 2\corona\CV_LatLon_21Jan_12Mar.csv')

#choosing columns from needed
df3 = df2[["country","lat","lon"]]

#aggregating 2 dataframes to get the coordinates of the coutries
df4=pd.merge(df,df3, on="country")
df4.drop_duplicates(keep="first",inplace=True)
#df4

fig = go.Figure(data=go.Scattergeo(
        lon = df4['lon'],
        lat = df4['lat'],
        text= df4[['country',"total_confirmed"]]
        ))

fig.update_layout(
     geo_scope="world",
    )
if st.checkbox("Show World Map"):
    st.write("Hover the map to check total confirmed cases in each country")
    fig

# Create a new dataframe to aggregate the data by continent

st.subheader("COVID-19 statistics by continent")
df1=df.groupby(['continent']).sum().reset_index()
trace_corona = go.Bar(x=df1.continent,
                  y=df1.total_confirmed,
                  name='Total cases',
                  marker=dict(color='#ffcdd2'))

trace_deaths = go.Bar(x=df1.continent,
                y=df1.total_deaths,
                name='Total death',
                marker=dict(color='#A2D5F2'))

trace_recovered = go.Bar(x=df1.continent,
                y=df1.total_recovered,
                name='Total recovered',
                marker=dict(color='#59606D'))

trace_active_cases = go.Bar(x=df1.continent,
                y=df1.active_cases,
                name='Active cases',
                marker=dict(color='#59600D'))


data = [trace_corona, trace_deaths, trace_recovered,trace_active_cases]

layout = go.Layout(#title="Corona Distribution Per Continent",
                xaxis=dict(title='Continent'),
                yaxis=dict(title='Number of cases'))

fig = go.Figure(data=data, layout=layout)
if st.checkbox("Show continents statistics"):
    fig

# Select continent to plot its contries total recoved and confirmed corona cases
st.subheader("COVID-19 country profiles")
if st.checkbox("Show country profiles"):

        option = st.selectbox(
        'Search by continent...'.upper(),
        df["continent"].unique()
        )

        filtered_data = df[df['continent']== option]

        fig = px.bar(filtered_data, x='country', y=["total_recovered","total_confirmed"])
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=200),paper_bgcolor="LightSteelBlue")
        fig

# scatterplot
st.subheader("COVID-19 Confirmed cases vs Countries population ")
if st.checkbox("Show Trendlines"):
    st.write("hover the graph for country names")

    fig1=px.scatter(df, x="population", y="total_confirmed",
    color="continent",range_x=[0,60000000], range_y=[0,500000],hover_name="country",
    trendline="ols")
    fig1

#Insights
expander = st.beta_expander("Insights")
expander.write("Europe, North America and South America countries have obviously higher confirmed rates with less population rates compared to other continents. These continents are clearly the riskier, but the main question remains WHY? Is it related to the area of the country vs its population? Is it related to the culture and the way of living? Is it related to the governement taking appropriate measures of safety? More research should be conducted to find the main factors affecting the pandemic spread!")
