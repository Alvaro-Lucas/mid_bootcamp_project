from folium import Map, Marker
from fpdf import FPDF, HTMLMixin
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st
import pandas as pd
import re
import requests
import json

class FPDF(FPDF, HTMLMixin):
    pass

def get_data_db(query):
    url = f"http://127.0.0.1:3500/get"
    res = requests.get(url+f"?{query}")
    if res.status_code >= 200 and res.status_code <= 300:
        return res.json()
    raise ValueError(f"Error {res.status_code} al obtener los datos de la base de datos")

def covid_cases_graph(data, periodo=30):
    covid_cases_date = pd.DataFrame(data)
    covid_cases_date = covid_cases_date.drop(columns=["_id", "Lat", "Long"])
    plt.figure(figsize=[20,20])

    for country in covid_cases_date.values:
        deaths = [int(death) for death in country[1::periodo]]
        plt.ylabel('Deaths')
        plt.xlabel('Date')
        plt.plot(covid_cases_date.columns[1::periodo], deaths, label=country[0])
        plt.legend()

    return plt

def geospatial_data(data):
    dataframe = pd.DataFrame(data)
    countries_geo = []
    for country in dataframe.itertuples():
        geo = {}
        geo["Country/Region"] = country[2]
        geo["geometry"] = {"type": "MultiPolygon", "coordinates": [country[3], country[4]]}
        countries_geo.append(geo)
    print(f"{countries_geo = }")
    return countries_geo

def geospatial_map(geospatial):
    m = Map()
    for country in geospatial:
        Marker(location=country["geometry"]["coordinates"], tooltip=country["Country/Region"]).add_to(m)
    folium_static(m)
    

st.title("Covid Dashboard Information")
data = get_data_db("project=Country/Region")

countries = [element["Country/Region"] for element in data]

chosen = st.multiselect('Countries', countries)
st.text('Enter the range of days between the dates (if boths are set at 0, the range will be 7 days)')
column = st.beta_columns(2)
with column[0]:
    periodo_days = st.slider('Days', min_value=0, max_value=30)  
with column[1]:
    periodo_months = st.slider('Months', min_value=0, max_value=12)  

if chosen:
    query = f"Country/Region="
    for i in chosen:
        query += i+","
    query = query[:-1]

    data = get_data_db(query)

    periodo = periodo_days + periodo_months*30
    if periodo == 0 or periodo > len(data[0])-4:
        periodo = 7
    
    plt = covid_cases_graph(data, periodo)
    st.pyplot(plt)

    geospatial = geospatial_data(data)
    geospatial_map(geospatial)

if st.button('Download PDF'):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.output('Covid_Cases_Dashboard.pdf', "I")
