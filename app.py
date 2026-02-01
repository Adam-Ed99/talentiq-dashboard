import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# =============================
# 1. ELITE DESIGN CONFIG
# =============================
st.set_page_config(
    page_title="TalentIQ AI | Market Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection de CSS personnalisé pour un look Unique
st.markdown("""
    <style>
    /* Global Background & Font */
    .main { background-color: #f8f9fa; }
    
    /* Custom Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0e1117 !important;
        border-right: 1px solid #FFD700;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        color: #1E88E5;
        font-size: 2.5rem !important;
        font-weight: 700;
    }
    
    /* Premium Cards */
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-bottom: 3px solid #FFD700;
    }
    
    /* Professional Tables */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Unique Header */
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #0e1117;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# =============================
# 2. SUPABASE & AUTH (Conservé)
# =============================
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY")

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# (Gestion Session State et Login identique à ta version actuelle)
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# =============================
# 3. SIDEBAR NAVIGATION
# =============================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3649/3649393.png", width=80) # Logo temporaire
    st.markdown("<h2 style='color: white; text-align: center;'>TALENTIQ ELITE</h2>", unsafe_allow_html=True)
    st.divider()
    
    if not st.session_state.user_email:
        email_in = st.text_input("Professional Email")
        pass_in = st.text_input("Access Key", type="password")
        if st.button("AUTHENTICATE 🚀", use_container_width=True):
            try:
                res = supabase.auth.sign_in_with_password({"email": email_in, "password": pass_in})
                st.session_state.user_email = res.user.email
                st.rerun()
            except:
                st.error("Invalid Credentials")
    else:
        st.success(f"Verified: {st.session_state.user_email}")
        if st.button("Sign Out"):
            st.session_state.user_email = None
            st.rerun()

# =============================
# 4. MAIN INTERFACE
# =============================
if st.session_state.user_email:
    # --- SUBSCRIPTION CHECK ---
    res = supabase.table("customers").select("subscription_status").eq("email", st.session_state.user_email).execute()
    if not res.data or res.data[0]["subscription_status"] != "active":
        st.warning("⚠️ Access Restricted: Active Subscription Required.")
        st.stop()

    # --- TOP HEADER ---
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("<h1 class='main-header'>🎯 Premium Market Intelligence</h1>", unsafe_allow_html=True)
        st.caption("DIGISPHERELLC LLC — Data Engineering & Global Sourcing")
    
    # --- DATA ENGINE ---
    base_path = os.path.dirname(os.path.abspath(__file__))
    # On scanne les CSV à la racine
    csv_files = [f for f in os.listdir(base_path) if f.endswith('.csv')]

    if csv_files:
        st.markdown("### 📂 Database Selection")
        selected_dataset = st.selectbox("", csv_files, label_visibility="collapsed")
        
        if selected_dataset:
            file_path = os.path.join(base_path, selected_dataset)
            df = pd.read_csv(file_path)

            # --- ANALYTICS OVERVIEW ---
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Records", f"{len(df):,}")
            # Exemple de stats dynamiques (si colonnes présentes)
            if 'location' in df.columns:
                m2.metric("Regions Coverage", df['location'].nunique())
            if 'company' in df.columns:
                m3.metric("Companies", df['company'].nunique())
            m4.metric("Status", "LATEST UPDATE")

            # --- CONTENT AREA ---
            tab1, tab2, tab3 = st.tabs(["💎 Data Explorer", "🔍 Advanced Search", "📥 Export Hub"])
            
            with tab1:
                st.markdown("#### High-Fidelity Data Preview")
                st.dataframe(df.head(100), use_container_width=True, height=500)
            
            with tab2:
                search_query = st.text_input("⚡ Power Search (Type any skill, name or city...)", placeholder="Ex: Python, London, Senior...")
                if search_query:
                    mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
                    st.dataframe(df[mask], use_container_width=True)
            
            with tab3:
                st.markdown("<div style='text-align: center; padding: 50px;'>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 DOWNLOAD ENTIRE DATASET (CSV)",
                    data=df.to_csv(index=False),
                    file_name=f"TalentIQ_{selected_dataset}",
                    mime="text/csv",
                    use_container_width=True
                )
                st.info("The downloaded file is optimized for Excel and Google Sheets.")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("No intelligence assets found in the repository.")
else:
    # Page d'accueil style "Landing Page"
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Unlock Global Talent Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>The exclusive platform for elite recruiters and data-driven firms.</p>", unsafe_allow_html=True)
