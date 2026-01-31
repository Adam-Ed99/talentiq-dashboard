import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# =============================
# 1. PAGE CONFIG
# =============================
st.set_page_config(
    page_title="TalentIQ AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# 2. SUPABASE CONFIG
# =============================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY")

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# =============================
# 3. GESTION DU RESET MOT DE PASSE
# =============================
query_params = st.query_params
if "type" in query_params and query_params["type"] == "recovery":
    st.title("🔄 Reset your password")
    new_password = st.text_input("New Password", type="password")
    if st.button("Update Password"):
        try:
            supabase.auth.update_user({"password": new_password})
            st.success("✅ Password updated! Log in from the sidebar.")
            st.query_params.clear()
        except Exception as e:
            st.error(f"Error: {str(e)}")
    st.stop()

# =============================
# 4. AUTH LOGIC
# =============================
if "user_email" not in st.session_state:
    st.session_state.user_email = None

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user_email = res.user.email
        st.rerun()
    except Exception as e:
        st.error(f"❌ Login failed: {str(e)}")

# =============================
# 5. SIDEBAR
# =============================
with st.sidebar:
    st.title("🔐 TalentIQ")
    if not st.session_state.user_email:
        email_in = st.text_input("Email")
        pass_in = st.text_input("Password", type="password")
        if st.button("Login 🚀"):
            login(email_in, pass_in)
    else:
        st.success(f"Logged in: {st.session_state.user_email}")
        if st.button("🚪 Logout"):
            st.session_state.user_email = None
            st.rerun()

# =============================
# 6. MAIN APP
# =============================
if st.session_state.user_email:
    # --- CHECK SUBSCRIPTION ---
    res = supabase.table("customers").select("subscription_status").eq("email", st.session_state.user_email).execute()
    if not res.data or res.data[0]["subscription_status"] != "active":
        st.warning("❌ Active subscription required.")
        st.stop()

    # --- DASHBOARD & DATASETS ---
    st.title("🎯 TalentIQ Premium Dashboard")
    
    # Correction : On cherche les fichiers à la RACINE (base_path)
    base_path = os.path.dirname(os.path.abspath(__file__))
    csv_files = [f for f in os.listdir(base_path) if f.endswith('.csv')]

    if csv_files:
        selected_dataset = st.selectbox("Select a Dataset to analyze:", csv_files)
        
        if selected_dataset:
            file_path = os.path.join(base_path, selected_dataset)
            df = pd.read_csv(file_path)

            tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Search", "📤 Export"])
            
            with tab1:
                st.metric("Total Profiles", len(df))
                st.dataframe(df.head(100), use_container_width=True)
            
            with tab2:
                query = st.text_input("Filter data (name, city, skill...)")
                if query:
                    mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
                    st.dataframe(df[mask], use_container_width=True)
            
            with tab3:
                st.download_button("📥 Download This Dataset", df.to_csv(index=False), file_name=selected_dataset)
    else:
        st.error("No CSV files found in the root directory.")
else:
    st.title("👋 Welcome to TalentIQ")
    st.info("Please sign in to access your premium data.")
