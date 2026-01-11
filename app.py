import streamlit as st
from supabase import create_client, Client
import os
import pandas as pd

# Supabase (Elest.io env vars)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

supabase = init_supabase()

def get_current_user():
    try:
        return supabase.auth.get_user().user
    except:
        return None

# MAIN
st.set_page_config(page_title="TalentIQ AI", layout="wide")

user = get_current_user()

# Check abonnement APRÈS login
if user:
    customer = supabase.table("customers").select("*").eq("email", user.email).single()
    if not customer.data or customer.data.get("subscription_status") != "active":
        st.error("❌ Abonnement Payhip requis")
        st.stop()

# Sidebar
with st.sidebar:
    st.title("🔐 TalentIQ")
    
    if not user:
        st.subheader("Sign In")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            try:
                supabase.auth.sign
