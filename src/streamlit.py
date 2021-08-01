import streamlit as st
import pandas as pd
import re
import requests
import json

st.title("Primera pruebas")
url = f"http://127.0.0.1:3500/all"
res = requests.get(url)
data = {}
#print(f"{res.json() = }")
#element_list = json.loads(res.json())
#print(len(res.json()))
for element in list(res.json()):
    #print(f"{element['abilities'] = }")
    for k in element.keys():
        data[k] = []
    for k, v in element.items():
        data[k] =.append(v)
#print(f"{data = }")
#df = pd.DataFrame(res.json())


#st.dataframe(df)