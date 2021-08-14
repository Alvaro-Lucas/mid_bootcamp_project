from pages.covid_world import worldwide
from folium import Map, Marker, folium
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

def get_data_db(query, db_collection = None):
    if db_collection:
        url = f"http://127.0.0.1:3500/get/{db_collection}"
    else:
        url = f"http://127.0.0.1:3500/get"

    res = requests.get(url+f"?{query}")
    if res.status_code >= 200 and res.status_code <= 300:
        return res.json()
    raise ValueError(f"Error {res.status_code} al obtener los datos de la base de datos")

def covid_cases_graph(data, periodo=30):
    covid_cases_date = pd.DataFrame(data)
    covid_cases_date = covid_cases_date.drop(columns=["_id", "Lat", "Long"])
    plt.figure(figsize=[20,10])
    columns = [column for column in covid_cases_date.columns[1::periodo]]
    for country in covid_cases_date.values:
        cases = [int(case) for case in country[1::periodo]]
        plt.ylabel('Cases')
        plt.xlabel('Date')
        plt.plot(columns, cases, label=country[0])
        plt.legend()
    return plt

def geospatial_data(data):
    dataframe = pd.DataFrame(data)
    countries_geo = []
    for country in dataframe.itertuples():
        geo = {}
        geo["Name"] = country[1]
        geo["geometry"] = {"type": "MultiPolygon", "coordinates": [country[2], country[3]]}
        countries_geo.append(geo)
    return countries_geo

def geospatial_map(geospatial):
    m = Map()
    for country in geospatial:
        Marker(location=country["geometry"]["coordinates"], tooltip=country["Name"]).add_to(m)
    folium_static(m)

def group_data(deaths = False, vaccination = False, ccaa_data = None, ccaa_vac = None):
    list_show = []
    dataframe_show = pd.DataFrame()

    if deaths:
        if vaccination:
            num_ccaa = len(ccaa_vac)
            for ccaa in range(num_ccaa):
                data_show = {}
                for key,value in ccaa_data[ccaa].items():
                    data_show[key] = str(value)

                for key,value in ccaa_vac[ccaa].items():
                    data_show[key] = str(value)

                data_show.pop("_id")
                data_show.pop("Fecha")
                list_show.append(data_show)
            dataframe_show = pd.DataFrame(list_show)
        else:
            num_ccaa = len(ccaa_data)
            for ccaa in range(num_ccaa):
                data_show = {}
                for key,value in ccaa_data[ccaa].items():
                    data_show[key] = str(value)
                data_show.pop("_id")
                list_show.append(data_show)
            dataframe_show = pd.DataFrame(list_show)
    else:
        if vaccination:
            num_ccaa = len(ccaa_vac)
            for ccaa in range(num_ccaa):
                data_show = {}
                for key,value in ccaa_vac[ccaa].items():
                    data_show[key] = str(value)
                data_show.pop("_id")
                data_show.pop("Fecha")
                list_show.append(data_show)
            dataframe_show = pd.DataFrame(list_show)
    return dataframe_show
    
st.markdown("<h1 style='text-align:center'><b>Covid Dashboard Information</b></h1>", unsafe_allow_html=True)

pages = st.sidebar.radio("Select the range of the Covid pandemic: ", ["Worldwide", "Spain, Autonomous Community"])

if pages == "Worldwide":
    worldwide

if pages == "Spain, Autonomous Community":
    data = get_data_db("All&project=Community", "ccaa_data")

    ca_names = [element["Community"] for element in data]
    ca_names.insert(0,"All")

    chosen = st.multiselect('Covid at the Autonomous Community in Spain', ca_names)

    selection = ["Deaths", "Vaccination"]
    default = [True, False]
    st.write("You must choose one or both if you want the data to show")
    data_info = st.beta_columns(2)
    with data_info[0]:
        deaths_checkbox = st.checkbox("Deaths")
    with data_info[1]:
        vaccination_checkbox = st.checkbox("Vaccination")

    ccaa_data = None
    ccaa_vac = None
    if chosen:
        if "All" in chosen:
            if deaths_checkbox:
                ccaa_data = get_data_db("All","ccaa_data")
            if vaccination_checkbox:
                ccaa_vac = get_data_db("All","ccaa_vac")
        else:
            query = f"Community="
            for i in chosen:
                query += i+","
            query = query[:-1]
            if deaths_checkbox:
                ccaa_data = get_data_db(query,"ccaa_data")
            if vaccination_checkbox:
                ccaa_vac = get_data_db(query,"ccaa_vac")

        dataframe_show = group_data(deaths_checkbox, vaccination_checkbox, ccaa_data, ccaa_vac)

        if not dataframe_show.shape[0] == 0:
            st.dataframe(dataframe_show)
            geospatial = geospatial_data(dataframe_show)
            geospatial_map(geospatial)

    cols = st.beta_columns((2,1,2))
    with cols[1]:
        if st.button('Download PDF'):
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font('Arial', 'BIU', 16)
            pdf.write(16,"Data in JSON format\n")

            pdf.set_font('Arial', '', 9)
            column_ccaa = []
            for column in dataframe_show.columns:
                column_ccaa.append(column)

            num_ccaa = 0
            pdf.write(5, "\n{")
            for ccaa in dataframe_show.values:
                pdf.write(5, "\n    {\n")
                for element in range(len(column_ccaa)):
                    if element == len(column_ccaa)-1:
                        pdf.write(5, f'        "{column_ccaa[element]}" : {ccaa[element]}\n')
                    else:
                        pdf.write(5, f'        "{column_ccaa[element]}" : {ccaa[element]},\n')
                if num_ccaa == dataframe_show.shape[0] -1:
                    pdf.write(5, "    }\n")
                else:
                    pdf.write(5, "    },")
                num_ccaa += 1
            pdf.write(5, "}\n")
            
            pdf.output("Covid_Cases_CCAA_Dashboard.pdf",dest="F")

