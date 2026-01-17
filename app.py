import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# ==============================
# PAGE CONFIG (DOIT ÊTRE EN PREMIER)
# ==============================
st.set_page_config(
    page_title="TalentIQ AI Engine",
    layout="wide"
)

# ==============================
# SUPABASE SECRETS (STREAMLIT CLOUD)
# ==============================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY")

@st.cache_resource
def init_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("❌ Supabase secrets missing. Check Streamlit Cloud settings.")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# ==============================
# SESSION / USER
# ==============================
def get_current_user():
    try:
        response = supabase.auth.get_user()
        return response.user
    except Exception:
        return None

user = get_current_user()

# ==============================
# SIDEBAR AUTH
# ==============================
with st.sidebar:
    st.title("🔐 TalentIQ AI")

    if not user:
        st.subheader("Sign in")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login 🚀", use_container_width=True):
            try:
                supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                st.rerun()
            except Exception as e:
                st.error("Login failed")

    else:
        st.success(f"✅ {user.email}")
        if st.button("Logout 🚪", use_container_width=True):
            supabase.auth.sign_out()
            st.rerun()

# ==============================
# MAIN APP
# ==============================
if not user:
    st.header("Welcome to TalentIQ AI Engine")
    st.info("Please sign in to access premium datasets.")
    st.stop()

# ==============================
# SUBSCRIPTION CHECK
# ==============================
try:
    result = (
        supabase
        .table("customers")
        .select("subscription_status")
        .eq("email", user.email)
        .execute()
    )

    if not result.data or result.data[0]["subscription_status"] != "active":
        st.error("❌ Active subscription required.")
        st.stop()

except Exception:
    st.error("❌ Subscription system not configured.")
    st.stop()

# ==============================
# DASHBOARD
# ==============================
st.title("📊 TalentIQ Premium Dashboard")
st.caption("DIGISPHERE LLC — Market Intelligence Engine")

DATASET_FILE = "premium_architects.csv"

if not os.path.exists(DATASET_FILE):
    st.error(f"Dataset not found: {DATASET_FILE}")
    st.stop()

df = pd.read_csv(DATASET_FILE)

tab1, tab2, tab3 = st.tabs([
    "📊 Overview",
    "🔍 Search",
    "📤 Export"
])

with tab1:
    st.metric("Total Profiles", len(df))
    st.dataframe(df.head(100), use_container_width=True)

with tab2:
    search = st.text_input("Search by skill, role, city, country...")
    if search:
        filtered_df = df[
            df.astype(str)
            .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        ]
        st.dataframe(filtered_df, use_container_width=True)

with tab3:
    st.download_button(
        label="📥 Download full dataset",
        data=df.to_csv(index=False),
        file_name="talentiq_export.csv",
        mime="text/csv"
    )
