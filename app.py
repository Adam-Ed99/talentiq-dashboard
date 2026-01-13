import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")

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

user = get_current_user()

# Customer check APRÈS user
if user:
    try:
        customer = supabase.table("customers").select("*").eq("email", user.email).execute()
        if not customer.data or customer.data[0]["subscription_status"] != "active":
            st.warning("❌ Abonnement requis")
            st.stop()
    except:
        pass  # Ignore si table vide

# === MAIN ===
st.set_page_config(page_title="TalentIQ AI", layout="wide")

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
            except Exception as e:
                st.error(f"❌ Login failed: {e}")
        
        st.markdown("---")
        if st.button("Create Account"):
            st.info("Inscription via Supabase Dashboard")
            
    else:
        st.success(f"✅ {user.email}")
        if st.button("🚪 Logout", use_container_width=True):
            supabase.auth.sign_out()
            st.rerun()

# PROTÉGÉ
if user:
    st.title("🎯 TalentIQ Premium Dashboard")
    st.caption("DIGISPHERELLC LLC")
    
    # Datasets
    try:
        # CSV local (fallback)
        if os.path.exists("premium_architects.csv"):
            df = pd.read_csv("premium_architects.csv")
            st.sidebar.title("Datasets")
            st.success("✅ premium_architects.csv loaded")
            
            # Sidebar navigation
            page = st.sidebar.radio("View", ["Overview", "Search", "Export"])
            
            if page == "Overview":
                st.subheader("📊 Overview")
                st.dataframe(df.head(10))
                st.metric("Total Profiles", len(df))
                
            elif page == "Search":
                st.subheader("🔍 Search")
                search = st.text_input("Recherche")
                if search:
                    filtered = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False).any(), axis=1)]
                    st.dataframe(filtered)
                    
            elif page == "Export":
                st.subheader("📤 Export")
                st.download_button("Download CSV", df.to_csv(index=False), "premium_architects.csv")
                
        else:
            st.info("📁 Ajoute premium_architects.csv")
            
    except Exception as e:
        st.error(f"Erreur: {e}")
        st.info("Test local: streamlit run app.py")
        
else:
    st.info("👋 Connecte-toi pour datasets premium")

# Footer
st.markdown("---")
st.markdown("**DIGISPHERELLC LLC** - Tech Talent Intelligence")

