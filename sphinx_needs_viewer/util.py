import json
import urllib.request
import sys

import streamlit as st

@st.cache_data
def get_needs_data(needs_url):  # noqa: D103 
    try:
        with urllib.request.urlopen(needs_url) as url:  # noqa: S310
            return json.load(url)
    except Exception:
        sys.exit(0)

@st.cache_data
def get_prepared_needs(needs_url, max_needs=20):
    needs_raw_data = get_needs_data(needs_url)
    needs_data = needs_raw_data["versions"]["2.1.0"]["needs"]
    needs_data_reduced = {x['id']:x for x in list(needs_raw_data["versions"]["2.1.0"]["needs"].values())[0:max_needs]}
    return needs_data_reduced

@st.cache_data
def get_need(needs_url, need_id):
    needs_raw_data = get_needs_data(needs_url)
    needs_data = needs_raw_data["versions"]["2.1.0"]["needs"]
    try:
        return needs_data[need_id]
    except KeyError:
        return False
    
def get_needs_ids(needs_url):
    needs_raw_data = get_needs_data(needs_url)
    return needs_raw_data["versions"]["2.1.0"]["needs"].keys()