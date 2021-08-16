from utils.type_casting import list_to_str
from utils.process_data import data_merge
from config import URL_API
import streamlit as st
import requests

@st.cache
def countries_names():
    res = requests.get(f"{URL_API}/countries")
    c_names = [country["Country/Region"] for country in res.json()]
    return list(c_names)

@st.cache
def countries_total(db_collection, countries):
    res = requests.get(f"{URL_API}/{db_collection}/total/{list_to_str(countries)}")
    return list(res.json())

@st.cache
def date_countries_by_intervales(countries, interval):
    res = requests.get(f"{URL_API}/covid/{list_to_str(countries)}/date_interval?{interval}")
    return list(res.json())

@st.cache
def date_range_countries(countries, start, end):
    res = requests.get(f"{URL_API}/covid/{list_to_str(countries)}/date_range?Start={start}&End={end}")
    return list(res.json())

@st.cache
def date_range_countries_with_intervals(countries, start, end, interval):
    print(f"res: {URL_API}/covid/{list_to_str(countries)}/{interval}/date_range?Start={start}&End={end}")
    res = requests.get(f"{URL_API}/covid/{list_to_str(countries)}/{interval}/date_range?Start={start}&End={end}")
    return list(res.json())

@st.cache
def countries_coord(countries):
    res = requests.get(f"{URL_API}/coord/{list_to_str(countries)}")
    return list(res.json())

@st.cache
def total_all_db(countries):
    data = {
        "cases": countries_total("covid", countries),
        "deaths": countries_total("deaths", countries),
        "recovered": countries_total("recovered", countries)
    }
    return data

@st.cache
def community_names():
    res = requests.get(f"{URL_API}/ccaa_covid_data/communities")
    c_names = [country["Community"] for country in res.json()]
    return list(c_names)

@st.cache
def community_data(db_collection, communities, minus=""):
    res = requests.get(f"{URL_API}/{db_collection}/{list_to_str(communities)}/data{minus}")
    return list(res.json())

@st.cache
def community_coord(communities):
    res = requests.get(f"{URL_API}/{list_to_str(communities)}/coord")
    return list(res.json())

@st.cache
def selected_data(chosen, option, minus):
    data = {
        "deceased": community_data("ccaa_covid_data",chosen, f"?-={list_to_str(minus)}"),
        "vaccinated": community_data("ccaa_covid_vac", chosen, f"?-={list_to_str(minus)}"),
        "both": data_merge(community_data("ccaa_covid_data",chosen, f"?-={list_to_str(minus)}"), community_data("ccaa_covid_vac", chosen, f"?-={list_to_str(minus)}"))
    }
    return data[option]