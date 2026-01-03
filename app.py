import streamlit as st
from supabase import create_client, Client
import os

# Supabase credentials
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# === SESSION CHECK ===
def get_current_user():
    try:
        return supabase.auth.get_user().user
    except:
        return None

# === MAIN ===
st.set_page_config(page_title="TalentIQ AI", layout="wide")

user = get_current_user()

# Sidebar AUTH
with st.sidebar:
    st.title("🔐 TalentIQ")
    
    if not user:
        st.subheader("Sign In")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login 🚀", use_container_width=True):
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": email, "password": password
                })
                st.rerun()
            except:
                st.error("❌ Invalid credentials")
        
        # Sign up
        if st.button("Create Account"):
            st.switch_page("signup.py")  # Optionnel
            
    else:
        st.success(f"✅ {user.email}")
        if st.button("🚪 Logout", use_container_width=True):
            supabase.auth.sign_out()
            st.rerun()

# PROTÉGÉ
if user:
    st.title("🎯 TalentIQ Premium Dashboard")
    st.caption("DIGISPHERELLC LLC")
    
    # Tes imports + pages existants
    try:
        from loader import load_all_datasets
        from visuals import render_visuals
        from insights import render_insights
        from search_page import render_search
        from export_page import render_export
        
        datasets = load_all_datasets()
        
        st.sidebar.title("Datasets")
        dataset_name = st.sidebar.selectbox("Select", list(datasets.keys()))
        page = st.sidebar.radio("View", ["Overview", "Search", "Export"])
        
        df = datasets[dataset_name]
        
        if page == "Overview":
            render_insights(df)
            render_visuals(df)
        elif page == "Search":
            render_search(df)
        elif page == "Export":
            render_export(df)
            
    except ImportError as e:
        st.info(f"📁 Modules en cours: {e}")
        st.dataframe(pd.read_csv("premium_architects.csv"))
        
else:
    st.info("👋 Login pour datasets premium")

# Footer
st.markdown("---")
st.markdown("**DIGISPHERELLC LLC** - Tech Talent Intelligence")
