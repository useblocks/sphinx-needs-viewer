import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide",
)

st.markdown("""
# Welcome to Sphinx-Needs Data viewer! 👋
            
Please select an application from the left menu.
            
All Apps are just protoypes, to test the capabilities of streamlit.
            
## 📦 Single Need Viewer
This app also supports the URL paramter **id**, which 
allows to define the need object, which shall be shown directly after
loading the app.
            
Exammple: [https://sphinx-needs-viewer.streamlit.app/Single_Need_Viewer?id=FEATURE_1](Single_Need_Viewer?id=FEATURE_1)

""")