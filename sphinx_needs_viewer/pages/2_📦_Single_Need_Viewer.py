import json
import urllib.request

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

from util import get_need, get_needs_ids

NEEDS_URL = "https://sphinx-needs.readthedocs.io/en/latest/needs.json"

@st.cache_data
def get_needs_data(needs_url):  # noqa: D103
    with urllib.request.urlopen(needs_url) as url:  # noqa: S310
        return json.load(url)

url_params = st.query_params
initial_sidebar_state = "auto"
if "no_sidebar" in url_params.keys():
    initial_sidebar_state = "collapsed"


# Page config
st.set_page_config(
    page_title="Single Need Viewer",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state=initial_sidebar_state,
    menu_items={
        "Report a bug": "https://github.com/useblocks/sphinx-needs-viewer",
    },
)

# needs_url = st.text_input("**needs.json URL**", NEEDS_URL)
needs_url = NEEDS_URL
need_ids = get_needs_ids(needs_url)

if 'selected_id_index' not in st.session_state:
    st.session_state.selected_id_index = 0

if "id" in url_params:
    selectd_id = url_params['id']
    try:
        st.session_state.selected_id_index = list(need_ids).index(selectd_id)
    except ValueError:
        st.session_state.selected_id_index = 0 # ID not found

def next_need():
    st.session_state.selected_id_index += 1
def prior_need():
    if st.session_state.selected_id_index > 0:
        st.session_state.selected_id_index -= 1

col1, col2 = st.columns([1,2], gap="large")

with col1:
    if st.session_state.selected_id_index >= len(need_ids)-1:
        st.session_state.selected_id_index = len(need_ids) -1
    subcol1, subcol2, subcol3 = st.columns([5,1,1])
    with subcol1:
        need_id = option = st.selectbox(
            "2",need_ids, index=st.session_state.selected_id_index, label_visibility="collapsed")
        st.session_state.selected_id_index = list(need_ids).index(need_id)
    with subcol2:
        st.button("\-", type="secondary", on_click=prior_need)
    with subcol3:
        st.button("\+", type="secondary", on_click=next_need)

    need = get_need(needs_url, need_id)

with col1:
    st.markdown(f"""
status: **{need["status"]}** \\
links: {" ,".join("**"+x+"**" for x in need["links"])} \\
tags: {" ,".join("**"+x+"**" for x in need["tags"])}

doc:    **{need["docname"]}{need["doctype"]}** \\
sections: {" > ".join("**"+x+"**" for x in need["sections"])}


[Open Need](https://sphinx-needs.readthedocs.io/en/latest/{need["docname"]}.html#{need["id"]}) | 
[Edit Need](https://github.com/useblocks/sphinx-needs/edit/master/docs/{need["docname"]}{need["doctype"]})
""")

with col2:
    if not need:
        st.write(f"Need with ID {need_id}  ot found")
    else:
        st.markdown(f"""
## {need["id"]}: {need["title"]}
{need["description"]}
""")

    st.divider()
    st.write("**Complete need data**")
    st.dataframe(need, use_container_width=True)

# Remove streamlit banner
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            body {background-color: transparent !important;}
            div.stApp {background-color: transparent !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)