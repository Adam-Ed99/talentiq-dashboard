import streamlit as st
import pandas as pd

def render_visuals(df):
    st.subheader("📊 Market Signals")
    
    if df.empty:
        st.info("No data to visualize")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if "followers" in df.columns:
            st.metric("Top Follower", df["followers"].max())
            st.bar_chart(df["followers"].value_counts().sort_index().head(15))
    
    with col2:
        if "public_repos" in df.columns:
            st.metric("Top Repos", df["public_repos"].max())
            st.bar_chart(df["public_repos"].value_counts().sort_index().head(15))
    
    # Category analysis
    cat_cols = df.select_dtypes(include="object").columns
    if len(cat_cols) > 0:
        col = st.selectbox("Analyze category", list(cat_cols))
        st.bar_chart(df[col].value_counts().head(10))
