from pages.covid_world import worldwide
from pages.covid_aacc import aacc
import streamlit as st

    
st.markdown("<h1 style='text-align:center'><b>Covid Dashboard Information</b></h1>", unsafe_allow_html=True)

pages = st.sidebar.radio("Select the range of the Covid pandemic: ", ["Worldwide", "Spain, Autonomous Community"])

if pages == "Worldwide":
    worldwide()

if pages == "Spain, Autonomous Community":
    aacc()

