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
# SESSION STATE
# =============================
if "user" not in st.session_state:
    st.session_state.user = None

# =============================
# AUTH FUNCTIONS
# =============================
def login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.user = res.user
        st.rerun()
    except Exception:
        st.error("❌ Login failed. Check email or password.")

def logout():
    supabase.auth.sign_out()
    st.session_state.user = None
    st.rerun()

user = st.session_state.user

# =============================
# SIDEBAR AUTH UI
# =============================
with st.sidebar:
    st.title("🔐 TalentIQ")

    if not user:
        st.subheader("Sign in")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            login(email, password)
    else:
        st.success(f"✅ {user.email}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()

# =============================
# MAIN APP LOGIC
# =============================
if user:
    # ----- SUBSCRIPTION CHECK -----
    try:
        result = (
            supabase
            .table("customers")
            .select("subscription_status")
            .eq("email", user.email)
            .execute()
        )

        if not result.data or result.data[0]["subscription_status"] != "active":
            st.warning("❌ Active subscription required.")
            st.stop()

    except Exception:
        st.error("⚠️ Subscription system error.")
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
