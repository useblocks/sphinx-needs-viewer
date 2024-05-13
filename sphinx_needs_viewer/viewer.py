"""ubInsights test app."""

import json
import urllib.request
import sys

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

NEEDS_URL = "https://sphinx-needs.readthedocs.io/en/latest/needs.json"
NEEDS_OPTIONS_DEFAULT = ["id", "title", "status", "tags", "links", "docname"]

@st.cache_data
def get_needs_data(needs_url):  # noqa: D103
    with urllib.request.urlopen(needs_url) as url:  # noqa: S310
        return json.load(url)


st.set_page_config(
    page_title="Sphinx-Needs viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)
st.sidebar.image("https://sphinx-needs.readthedocs.io/en/latest/_images/sphinx-needs-logo-bg.png")

st.sidebar.markdown("""
## needs.json Viewer
This is a data viewer for the Traceability tool [Sphinx-Needs](https://sphinx-needs.readthedocs.io)

## Config
""")
needs_url = st.sidebar.text_input("**needs.json URL**", NEEDS_URL)

msg = st.toast("Fetching needs.json...")
try:
    needs_raw_data = get_needs_data(needs_url)
except Exception:
    msg.toast("Can't fetch data from provided URL!", icon="⚠")
    sys.exit(0)
msg.toast("Fetching done!", icon="🎉")

needs_data = needs_raw_data["versions"]["2.1.0"]["needs"]

max_needs = st.sidebar.slider("**Max. needs to show**", 0, len(needs_data), 5 if len(needs_data) >= 5 else 0)

needs_data_reduced = {x['id']:x for x in list(needs_raw_data["versions"]["2.1.0"]["needs"].values())[0:max_needs]}

needs_data_string = json.dumps(needs_data_reduced, indent=4)

needs_data_keys = []
selected_options = NEEDS_OPTIONS_DEFAULT
if needs_data_reduced:
    needs_data_keys = list(needs_data_reduced.values())[0].keys()

    selected_options = st.sidebar.multiselect(
        "**Options to show on table**",
        needs_data_keys,
        NEEDS_OPTIONS_DEFAULT,
    )

needs_data_configured = {}
for key, need in needs_data_reduced.items():
    needs_data_configured[key] = {x: y for x,y in need.items() if x in selected_options}

# Source link
st.markdown(f"Data source: [{needs_url}]({needs_url})")

# Table
st.subheader('Table')
st.markdown(f"Showing **{max_needs}** need objects:")
st.dataframe(needs_data_configured, use_container_width=True)

# FLOWCHART
nodes = []
edges = []

for key, need in needs_data_reduced.items():

    nodes.append( Node(id=key,
                    label=need["title"],
                    size=25))

    for link in need["links"]:
        if link in needs_data_reduced.keys():
            edges.append( Edge(source=key,   # noqa: PERF401
                            label="links",
                            target=link,
                            ))
config = Config(width=1000,
                height=500,
                directed=True, 
                physics=True, 
                hierarchical=False,
                # **kwargs
                )

st.markdown("""
## FlowChart
Use **mouse wheel** to zoom in/out.
""")
return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

# Data Tree
if st.sidebar.checkbox('Show data tree'):
    st.subheader('Data tree')
    st.json(needs_data_configured, expanded=False)

# Raw data code
if st.sidebar.checkbox('Show json raw data'):
    st.subheader('Raw data')
    needs_data_configured_string = json.dumps(needs_data_configured, indent=4)
    st.code(needs_data_configured_string, "json")
