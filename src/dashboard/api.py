#Methods that calling the API for data
import requests
from utils.type_casting import list_to_str
from utils.process_data import data_merge

def countries_names():
    res = requests.get("http://127.0.0.1:3500/covid/countries")
    c_names = [country["Country/Region"] for country in res.json()]
    return list(c_names)

def countries_total(db_collection, countries):
    res = requests.get(f"http://127.0.0.1:3500/{db_collection}/total/{list_to_str(countries)}")
    return list(res.json())

def data_graph(countries, interval):
    res = requests.get(f"http://127.0.0.1:3500/covid/{list_to_str(countries)}/date_interval?{interval}")
    return list(res.json())

def countries_coord(countries):
    res = requests.get(f"http://127.0.0.1:3500/coord/{list_to_str(countries)}")
    return list(res.json())

def total_all_db(countries):
    data = {
        "cases": countries_total("covid", countries),
        "deaths": countries_total("deaths", countries),
        "recovered": countries_total("recovered", countries)
    }
    return data


def community_names():
    res = requests.get("http://127.0.0.1:3500/ccaa_covid_data/communities")
    c_names = [country["Community"] for country in res.json()]
    return list(c_names)

def community_data(db_collection, communities, minus=""):
    res = requests.get(f"http://127.0.0.1:3500/{db_collection}/{list_to_str(communities)}/data{minus}")
    return list(res.json())

def community_coord(communities):
    res = requests.get(f"http://127.0.0.1:3500/{list_to_str(communities)}/coord")
    return list(res.json())

def selected_data(chosen, option, minus):
    data = {
        "deceased": community_data("ccaa_covid_data",chosen, f"?-={list_to_str(minus)}"),
        "vaccinated": community_data("ccaa_covid_vac", chosen, f"?-={list_to_str(minus)}"),
        "both": data_merge(community_data("ccaa_covid_data",chosen, f"?-={list_to_str(minus)}"), community_data("ccaa_covid_vac", chosen, f"?-={list_to_str(minus)}"))
    }
    return data[option]