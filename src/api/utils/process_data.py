def get_data_in_range(countries_all_data, range_date):
    data = []
    for country in countries_all_data:
        between_range = False
        country_data_range = {}
        country_data_range["Country/Region"] = country["Country/Region"]
        for date in country.keys():
            if date == range_date["Start"]:
                between_range = True
            if date == range_date["End"] and between_range:
                between_range = False
                country_data_range[date] = country[date]
            if between_range:
                country_data_range[date] = country[date]
        data.append(country_data_range)
    return data

def apply_interval(countries_all_data, interval):
    data = []
    
    try:
        countries_all_data.pop("Lat")
        countries_all_data.pop("Long")
    except:
        pass

    for country in countries_all_data:
        countries_refactor = {}
        countries_refactor["Country/Region"] = country["Country/Region"]
        for column in list(country.keys())[1::interval]:
            countries_refactor[column] = country[column]
        data.append(countries_refactor)
    return data