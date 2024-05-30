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

needs_url = st.text_input("**needs.json URL**", NEEDS_URL)
need_ids = get_needs_ids(needs_url)
selected_id_index = 0
if "id" in url_params:
    selectd_id = url_params['id']
    try:
        selected_id_index = list(need_ids).index(selectd_id)
    except ValueError:
        selected_id_index = 0 # ID not found

need_id = option = st.selectbox(
    "Needs ID",need_ids, index=selected_id_index)
need = get_need(needs_url, need_id)


if not need:
    st.write(f"Need with ID {need_id}  ot found")
else:
    st.markdown(f"""
## {need["id"]}: {need["title"]}
status: **{need["status"]}**

doc: **{need["docname"]}{need["doctype"]}**

link: https://sphinx-needs.readthedocs.io/en/latest/{need["docname"]}.html#{need["id"]}

{need["description"]}
""")

    st.dataframe(need, use_container_width=True)