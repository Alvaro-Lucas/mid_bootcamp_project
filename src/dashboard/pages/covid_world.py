from api import countries_names, countries_total, date_countries_by_intervales, countries_coord, total_all_db, date_range_countries, date_range_countries_with_intervals
from utils.show_functions import *
from utils.process_data import change_key_name, covid_cases_graph


def worldwide():
    countries = countries_names()
    
    moddifier = st.select_slider('Select the type of moddifier to apply', options=['Interval','Range of date', 'Interval in range date'])
    
    chosen = st.multiselect('Countries', countries)

    if moddifier == 'Range of date':
        start, end = rage_date_option()
    else:
        interval = interval_option()
        if interval == 0:
            interval = 1
        if moddifier == 'Interval in range date':
            start, end = rage_date_option()

    if chosen:
        data_total = total_all_db(chosen)

        data_table = [(data_total["cases"], "blue"), (data_total["deaths"], "red"), (data_total["recovered"], "green")]
        total_show(chosen, data_table)

        if moddifier == 'Interval':
            data = date_countries_by_intervales(chosen, interval)
        else:
            if moddifier == 'Range of date':
                data = date_range_countries(chosen, start, end)
            else:
                data = date_range_countries_with_intervals(chosen, start, end, interval)

        plt = covid_cases_graph(data)
        
        st.pyplot(plt)

        geospatial_data = countries_coord(chosen)
        geospatial_map(change_key_name(geospatial_data, "Country/Region", "Name"))

        '''
        cols = st.beta_columns((2,1,2))
        with cols[1]:
            if st.button('Download PDF'):
                pdf_screenshot("Covid_WorldWide")
        '''