import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# =============================
# PAGE CONFIG (TOUJOURS EN PREMIER)
# =============================
st.set_page_config(
    page_title="TalentIQ AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# SUPABASE CONFIG
# =============================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY")


@st.cache_resource
def init_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("❌ Supabase secrets missing. Check Streamlit Cloud settings.")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# =============================
# SESSION STATE AVEC PERSISTANCE
# =============================
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# =============================
# AUTH FUNCTIONS AVEC PERSISTANCE
# =============================
def login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        # STOCKAGE PERSISTANT dans session_state
        st.session_state.user_email = res.user.email
        st.session_state.user_id = res.user.id
        st.success("✅ Login successful!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Login failed: {str(e)}")

def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    # Nettoyage session
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.rerun()

# Récupération de l'utilisateur depuis session_state
user_email = st.session_state.user_email

# =============================
# SIDEBAR AUTH UI
# =============================
with st.sidebar:
    st.title("🔐 TalentIQ")

    if not user_email:
        st.subheader("Sign in")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            if email and password:
                login(email, password)
            else:
                st.warning("Please enter email and password")
    else:
        st.success(f"✅ {user_email}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()

# =============================
# MAIN APP LOGIC
# =============================
if user_email:
    # ----- SUBSCRIPTION CHECK -----
    try:
        result = (
            supabase
            .table("customers")
            .select("subscription_status")
            .eq("email", user_email)
            .execute()
        )

        if not result.data or result.data[0]["subscription_status"] != "active":
            st.warning("❌ Active subscription required.")
            st.info("Contact support@digispherellc.com to activate your subscription.")
            st.stop()

    except Exception as e:
        st.error(f"⚠️ Subscription system error: {str(e)}")
        st.stop()

    # ----- DASHBOARD -----
    st.title("🎯 TalentIQ Premium Dashboard")
    st.caption("DIGISPHERELLC LLC — Market Intelligence")

    DATASETS_DIR = "datasets"

    # Scan for CSV files
    try:
        csv_files = [f for f in os.listdir(DATASETS_DIR) if f.endswith('.csv')]
    except FileNotFoundError:
        st.error(f"Directory not found: '{DATASETS_DIR}'")
        st.stop()

    if not csv_files:
        st.warning(f"No CSV datasets found in '{DATASETS_DIR}'.")
        st.stop()
    
    selected_dataset = st.selectbox("Select a Dataset to analyze:", csv_files)
    
    if selected_dataset:
        dataset_path = os.path.join(DATASETS_DIR, selected_dataset)
        df = pd.read_csv(dataset_path)

        tab1, tab2, tab3 = st.tabs([
            "📊 Overview",
            "🔍 Search",
            "📤 Export"
        ])

        with tab1:
            st.metric("Total Profiles", len(df))
            st.dataframe(df.head(50), use_container_width=True)

        with tab2:
            query = st.text_input("Search by name, skill or city")
            if query:
                filtered_df = df[
                    df.astype(str)
                    .apply(lambda row: row.str.contains(query, case=False).any(), axis=1)
                ]
                st.dataframe(filtered_df, use_container_width=True)

        with tab3:
            st.download_button(
                f"📥 Download {selected_dataset}",
                df.to_csv(index=False),
                file_name=selected_dataset,
                mime="text/csv"
            )

else:
    st.title("👋 Welcome to TalentIQ")
    st.info("Please sign in from the sidebar to access premium datasets.")
