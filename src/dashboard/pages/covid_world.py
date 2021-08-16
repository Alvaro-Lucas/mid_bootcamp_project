from api import countries_names, countries_total, date_countries_by_intervales, countries_coord, total_all_db
from utils.show_functions import *
from utils.process_data import change_key_name


def worldwide():
    countries = countries_names()

    chosen = st.multiselect('Countries', countries)

    st.text('Enter the range of days between the dates (if boths are set at 0, the range will be 7 days)')
    interval = 0
    column = st.beta_columns(2)
    with column[0]:
        interval += st.slider('Days', min_value=0, max_value=30)  
    with column[1]:
        interval += st.slider('Months', min_value=0, max_value=12)*30
    
    if interval == 0:
        interval = 7

    if chosen:
        data_total = total_all_db(chosen)

        data_table = [(data_total["cases"], "blue"), (data_total["deaths"], "red"), (data_total["recovered"], "green")]
        total_show(chosen, data_table)

        plt = covid_cases_graph(date_countries_by_intervales(chosen, interval))

        st.pyplot(plt)

        geospatial_data = countries_coord(chosen)
        geospatial_map(change_key_name(geospatial_data, "Country/Region", "Name"))

        cols = st.beta_columns((2,1,2))
        with cols[1]:
            if st.button('Download PDF'):
                pdf_screenshot("Covid_WorldWide")