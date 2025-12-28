import streamlit as st

def render_insights(df):
    st.subheader("🧠 AI Insights")

    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Profiles", len(df))
    
    if "followers" in df.columns:
        col2.metric("Avg Followers", f"{df['followers'].mean():.0f}")
    
    if "public_repos" in df.columns:
        col3.metric("Avg Repos", f"{df['public_repos'].mean():.0f}")
    
    if "location" in df.columns:
        remote_count = df["location"].str.contains("Remote", case=False, na=False).sum()
        col4.metric("% Remote", f"{100*remote_count/len(df):.0f}%")

    if "location" in df.columns:
        st.write("**Top locations:**", 
                df["location"].value_counts().head(5).index.tolist())
