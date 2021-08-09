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
        geo["Country/Region"] = country[2]
        geo["geometry"] = {"type": "MultiPolygon", "coordinates": [country[3], country[4]]}
        countries_geo.append(geo)
    return countries_geo

def geospatial_map(geospatial):
    m = Map()
    for country in geospatial:
        Marker(location=country["geometry"]["coordinates"], tooltip=country["Country/Region"]).add_to(m)
    folium_static(m)

def show_dataframe(deaths, vaccination, ccaa_data, ccaa_vac):
    list_show = []
    if deaths:
        if vaccination:
            for ccaa in range(len(ccaa_data)):
                data_show = {}
                for key,value in ccaa_data[ccaa].items():
                    data_show[key] = str(value)

                for key,value in ccaa_vac[ccaa].items():
                    data_show[key] = str(value)

                data_show.pop("_id")
                data_show.pop("Fecha")
                list_show.append(data_show)
            dataframe_show = pd.DataFrame(list_show)
            st.dataframe(dataframe_show)
        else:
            for ccaa in range(len(ccaa_data)):
                data_show = {}
                for key,value in ccaa_data[ccaa].items():
                    data_show[key] = str(value)
                data_show.pop("_id")
                list_show.append(data_show)
            dataframe_show = pd.DataFrame(list_show)
            st.dataframe(dataframe_show)
    else:
        if vaccination:
            for ccaa in range(len(ccaa_data)):
                data_show = {}
                for key,value in ccaa_vac[ccaa].items():
                    data_show[key] = str(value)
                data_show.pop("_id")
                data_show.pop("Fecha")
                list_show.append(data_show)
            dataframe_show = pd.DataFrame(list_show)
            st.dataframe(dataframe_show)
    
st.markdown("<h1 style='text-align:center'><b>Covid Dashboard Information</b></h1>", unsafe_allow_html=True)

pages = st.sidebar.radio("Select the range of the Covid pandemic: ", ["Worldwide", "Spain, Autonomous Community"])

if pages == "Worldwide":
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

        data_global = get_data_db(query)
        query += "&project=Country/Region,Total"
        data_deaths = get_data_db(query,"deaths")
        data_recovered = get_data_db(query,"recovered")
        data_cases = get_data_db(query)

        periodo = periodo_days + periodo_months*30
        if periodo == 0 or periodo > len(data_global[0])-4:
            periodo = 7
        
        cases = pd.DataFrame(data = data_cases)
        deaths = pd.DataFrame(data = data_deaths)
        recovered = pd.DataFrame(data = data_recovered)

        for countries in chosen:
            st.markdown(f"\n<h3 style='text-align:center; background-color:orange;'><b>{countries}</b></h3>", unsafe_allow_html=True)
            data_countries_columns = st.beta_columns(3)
            with data_countries_columns[0]:
                st.markdown("<h2 style='text-align:center; background-color:blue;'><b>Cases</b></h2>", unsafe_allow_html=True)
                num_cases = list(cases[cases['Country/Region'] == countries].values[0])
                st.markdown(f"<p style='text-align:center'><b>{num_cases[1]}</b></p>", unsafe_allow_html=True)
            
            with data_countries_columns[1]:
                st.markdown("<h2 style='text-align:center; background-color:red;'><b>Deaths</b></h2>", unsafe_allow_html=True)
                num_deaths = list(deaths[deaths['Country/Region'] == countries].values[0])
                st.markdown(f"<p style='text-align:center'><b>{num_deaths[1]}</b></p>", unsafe_allow_html=True)

            with data_countries_columns[2]:
                st.markdown("<h2 style='text-align:center; background-color:green;'><b>Recovered</b></h2>", unsafe_allow_html=True)
                num_recovered = list(recovered[recovered['Country/Region'] == countries].values[0])
                st.markdown(f"<p style='text-align:center'><b>{num_recovered[1]}</b></p>", unsafe_allow_html=True)

        plt = covid_cases_graph(data_global, periodo)
        st.pyplot(plt)

        geospatial = geospatial_data(data_global)
        geospatial_map(geospatial)

if pages == "Spain, Autonomous Community":
    data = get_data_db("project=Community", "ccaa_data")

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
    
    if chosen:
        if "All" in chosen:
            ccaa_data = get_data_db("All","ccaa_data")
            ccaa_vac = get_data_db("All","ccaa_vac")
        else:
            query = f"Community="
            for i in chosen:
                query += i+","
            query = query[:-1]
            ccaa_data = get_data_db(query,"ccaa_data")
            ccaa_vac = get_data_db(query,"ccaa_vac")

        show_dataframe(deaths_checkbox, vaccination_checkbox, ccaa_data, ccaa_vac)
        
        geospatial = geospatial_data(ccaa_data)
        geospatial_map(geospatial)



cols = st.beta_columns((2,1,2))
with cols[1]:
    if st.button('Download PDF'):
        pdf = FPDF()
        pdf.add_page(orientation="L", format="A3")
        plt.savefig("Cases_dates.jpg")
        pdf.image("./Cases_dates.jpg", w=400, h=260)
        pdf.add_page()

        covid_cases_data = pd.DataFrame(data_global).drop(columns=["_id", "Lat", "Long"])
        num_case_date = []

        columns = [column for column in covid_cases_data.columns[1::periodo]]
        columns.insert(0,covid_cases_data.columns[0])
        for country in covid_cases_data.values: 
            cases = [int(case) for case in country[1::periodo]]
            cases.insert(0,country[0])
            num_case_date.append(cases)
        
        pdf.set_font('Arial', 'BIU', 16)
        pdf.write(16,"Data in JSON format\n")

        pdf.set_font('Arial', '', 9)
        for country in range(len(num_case_date)):
            if country == 0:
                pdf.write(5, "\n{")
            pdf.write(5, "\n    {\n")
            for position in range(len(columns)):
                if position == len(columns)-1:
                    pdf.write(5, f'        "{columns[position]}" : {num_case_date[country][position]}\n')
                else:
                    pdf.write(5, f'        "{columns[position]}" : {num_case_date[country][position]},\n')
            if country == len(num_case_date)-1:
                pdf.write(5, "    }\n")
                pdf.write(5, "}\n")
            else:
                pdf.write(5, "    },")
        
        pdf.output("Covid_Cases_Dashboard.pdf",dest="F")
