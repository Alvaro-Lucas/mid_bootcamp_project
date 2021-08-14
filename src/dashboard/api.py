#Methods that calling the API for data

def countries_names():
    res = requests.get("http://127.0.0.1:3500/covid/countries")
    return list(res.json)

def countries_data(db_collection, countries):
    string = list_to_str(countries)
    res = requests.get(f"http://127.0.0.1:3500/{db_collection}/data/{countries}")
    return list(res.json)

def countries_total(countries):