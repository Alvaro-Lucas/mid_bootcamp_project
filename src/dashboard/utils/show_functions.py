from folium import Map, Marker
from streamlit_folium import folium_static
from fpdf import FPDF, HTMLMixin
from selenium import webdriver
from utils.type_casting import datetime_to_m_d_y
import streamlit as st
import datetime

def total_show(chosen, data_table):
    cols = ["Total Cases", "Deaths", "Recovered"]
    for country in chosen:
        st.markdown(f"\n<h4 style='text-align:center; background-color:orange;'><b>{country}</b></h4>", unsafe_allow_html=True)
        data_countries_columns = st.columns(3)
        for i in range(3):
            with data_countries_columns[i]:
                total_show_columns(data_table[i][0], country, data_table[i][1], cols[i])

def total_show_columns(data, country, color, col_name):
    print(data)
    for i, c_cases in enumerate(data):
        if c_cases["Country/Region"] == country:
            st.markdown(f"<p style='text-align:center; background-color:{color};'><b>{col_name}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; background-color:grey;'><b>{c_cases['Total']}</b></p>", unsafe_allow_html=True)
            st.markdown(f"\n", unsafe_allow_html=True)
    

def geospatial_map(geospatial, start_location = None ):
    m = Map(start_location ,zoom_start=5)
    for location in geospatial:
        Marker(location=[location["Lat"], location["Long"]], tooltip=location["Name"]).add_to(m)
    folium_static(m)


def interval_option():
    st.text('Enter the range of days between the dates (if boths are set at 0, the range will be 7 days)')
    interval = 1
    interval_column = st.columns(2)
    with interval_column[0]:
        interval += st.slider('Days', min_value=0, max_value=30)  
    with interval_column[1]:
        interval += st.slider('Months', min_value=0, max_value=12)*30

    return interval

def rage_date_option():
    st.write("Select the range on the date that wanted to show:")
    date_range_column = st.columns(2)
    with date_range_column[0]:
        start = st.date_input('Star date',value = datetime.date(2020, 1, 22), min_value=datetime.date(2020, 1, 22), max_value=datetime.date(2021, 8, 4))
    with date_range_column[1]:
        end = st.date_input('End date', value = datetime.date(2021, 8, 4), min_value=datetime.date(2020, 1, 22), max_value=datetime.date(2021, 8, 4))
    
    return (datetime_to_m_d_y(start), datetime_to_m_d_y(end))

#No he podido hacerlo funcionar, selenium no me funciona
def pdf_screenshot(Name):
    browser = webdriver.Firefox()
    browser.get("http://172.20.240.113:8501")
    pdf = FPDF()
    pdf.add_page()
    pdf.image(browser.get_screenshot_as_file(f"{Name}_image.png"))
    browser.close()
    browser.quit()
    pdf.output(f"{Name}.pdf",dest="F")