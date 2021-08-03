import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st
import pandas as pd
import re
import requests
import json

st.title("Covid Dashboard Information")
query = "project=Country/Region"
url = f"http://127.0.0.1:3500/get"
res = requests.get(url+f"?{query}")
data = res.json()
countries = [element["Country/Region"] for element in data]
st.select_slider('Slide to select', options=[1,'2'])
chosen = st.multiselect('Countries', countries)
if chosen:
    query = f"Country/Region="
    for i in chosen:
        query += i+","
    query = query[:-1]
    res_print = requests.get(url+f"?{query}")
    data_print = []
    id_own = 0
    for element in res_print.json():
        element['id'] = id_own
        data_print.append(element)
        id_own += 1
    data_print = pd.DataFrame(data_print)
    plt.figure(figsize=[15,15])
    
    for country in data_print.values:
        deaths = [int(death) for death in country[4:-1:30]]
        plt.plot(data_print.columns[4:-1:30], deaths, label=country[1])
        plt.legend()
    st.pyplot(plt)

