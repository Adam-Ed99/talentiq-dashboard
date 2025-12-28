import streamlit as st
from loader import load_all_datasets
from visuals import render_visuals
from insights import render_insights

st.set_page_config(
    page_title="TalentIQ AI Engine",
    layout="wide",
    page_icon="📊"
)

st.title("TalentIQ AI Engine")
st.caption("Market Intelligence for Mission-Critical Tech Hiring")

datasets = load_all_datasets()

if not datasets:
    st.warning("No datasets detected.")
    st.stop()

dataset_name = st.sidebar.selectbox(
    "Select dataset",
    list(datasets.keys())
)

df = datasets[dataset_name]

render_insights(df)
render_visuals(df)
