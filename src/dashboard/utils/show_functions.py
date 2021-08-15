from folium import Map, Marker
from streamlit_folium import folium_static
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def total_show_columns(data, country, color):
    for c_cases in data:
        if c_cases["Country/Region"] == country:
            st.markdown(f"<h2 style='text-align:center; background-color:{color};'><b>Cases</b></h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center'><b>{c_cases['Total']}</b></p>", unsafe_allow_html=True)


def total_show(chosen, data_table):
    for country in chosen:
        st.markdown(f"\n<h3 style='text-align:center; background-color:orange;'><b>{country}</b></h3>", unsafe_allow_html=True)
        data_countries_columns = st.beta_columns(3)
        for i in range(3):
            with data_countries_columns[i]:
                total_show_columns(data_table[i][0], country, data_table[i][1])


def covid_cases_graph(data):
    covid_cases_date = pd.DataFrame(data)
    plt.figure(figsize=[20,10])
    columns = [column for column in covid_cases_date.columns[1:]]
    for country in covid_cases_date.values:
        plt.ylabel('Cases')
        plt.xlabel('Date')
        plt.plot(columns, country[1:], label=country[0])
        plt.legend()
    return plt
    

def geospatial_map(geospatial, start_location = None ):
    print(f"{geospatial =}")
    m = Map(start_location ,zoom_start=5)
    for location in geospatial:
        Marker(location=[location["Lat"], location["Long"]], tooltip=location["Name"]).add_to(m)
    folium_static(m)

def pdf_screenshot():
    #binary = FirefoxBinary(r"/mnt/c/Program\ Files/Mozilla\ Firefox/firefox.exe")
    browser = webdriver.Firefox("/mnt/c/Program Files/Mozilla Firefox/")
    browser.get('http://192.168.0.101:8501')

    browser.get_screenshot_as_file("screenshot.pdf")
    browser.quit()

