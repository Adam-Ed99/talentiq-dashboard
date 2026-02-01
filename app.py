import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# =============================
# 1. ELITE DESIGN CONFIG
# =============================
st.set_page_config(
    page_title="DIGISPHERE | Premium Data Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# 2. PREMIUM CSS INJECTION — DARK LUXURY THEME
# =============================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* ===== HIDE STREAMLIT BRANDING — KEEP SIDEBAR TOGGLE ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make header transparent but keep it functional for sidebar toggle */
    [data-testid="stHeader"] {
        background: transparent !important;
        border: none !important;
    }
    
    /* Hide toolbar and decoration, but not the collapse button */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    [data-testid="stDecoration"] {
        display: none !important;
    }
    .stDeployButton {
        display: none !important;
    }
    
    /* Style the sidebar collapse/expand button */
    button[data-testid="stBaseButton-headerNoPadding"],
    [data-testid="collapsedControl"] {
        background: rgba(124, 58, 237, 0.2) !important;
        border: 1px solid rgba(168, 139, 250, 0.3) !important;
        border-radius: 8px !important;
        color: #a78bfa !important;
    }
    
    button[data-testid="stBaseButton-headerNoPadding"]:hover,
    [data-testid="collapsedControl"]:hover {
        background: rgba(124, 58, 237, 0.4) !important;
    }
    
    /* ===== GLOBAL DARK THEME ===== */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #141420 50%, #0d0d15 100%) !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }
    
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
    }
    
    /* ===== SIDEBAR — PREMIUM DARK ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c0c14 0%, #12121c 100%) !important;
        border-right: 1px solid rgba(168, 139, 250, 0.15);
    }
    
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(168, 139, 250, 0.2) !important;
        border-radius: 12px !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput input {
        color: #f1f5f9 !important;
    }
    
    section[data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
    }
    
    /* ===== METRICS CARDS — GLASSMORPHISM ===== */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 139, 250, 0.1);
        border-radius: 16px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: rgba(168, 139, 250, 0.3);
        transform: translateY(-3px);
        box-shadow: 0 10px 40px rgba(124, 58, 237, 0.15);
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 50%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
    }
    
    /* ===== DATAFRAMES — PREMIUM TABLE ===== */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        border: 1px solid rgba(168, 139, 250, 0.1) !important;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: rgba(15, 15, 25, 0.8) !important;
    }
    
    /* ===== TABS — MODERN NAVIGATION ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 14px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #94a3b8 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* ===== BUTTONS — PREMIUM STYLE ===== */
    .stDownloadButton button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3) !important;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* ===== SELECT BOX ===== */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(168, 139, 250, 0.2) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }
    
    /* ===== TEXT INPUTS ===== */
    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(168, 139, 250, 0.2) !important;
        border-radius: 12px !important;
    }
    
    .stTextInput input {
        color: #e2e8f0 !important;
    }
    
    .stTextInput input::placeholder {
        color: #64748b !important;
    }
    
    /* ===== ALERTS ===== */
    .stAlert {
        border-radius: 14px !important;
        border: none !important;
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border-color: rgba(168, 139, 250, 0.1) !important;
        margin: 2rem 0 !important;
    }
    
    /* ===== CUSTOM HEADER CLASSES ===== */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 30%, #f0abfc 60%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0;
    }
    
    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(168, 139, 250, 0.2);
        border-radius: 50px;
        padding: 8px 18px;
        font-size: 0.8rem;
        color: #c4b5fd;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .section-title {
        color: #e2e8f0;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-title::before {
        content: '';
        width: 4px;
        height: 24px;
        background: linear-gradient(180deg, #7c3aed 0%, #a855f7 100%);
        border-radius: 2px;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }
    
    /* ===== LANDING PAGE ===== */
    .landing-container {
        text-align: center;
        padding: 4rem 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .landing-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
    }
    
    .landing-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .landing-desc {
        color: #94a3b8;
        font-size: 1.2rem;
        line-height: 1.8;
        margin-bottom: 2rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin-top: 3rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(168, 139, 250, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: rgba(168, 139, 250, 0.3);
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-title {
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* ===== LOGO STYLING ===== */
    .sidebar-brand {
        text-align: center;
        padding: 1rem 0 1.5rem 0;
    }
    
    .sidebar-logo {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 2px;
    }
    
    .sidebar-subtitle {
        color: #4a5568;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 4px;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(124, 58, 237, 0.2); }
        50% { box-shadow: 0 0 40px rgba(124, 58, 237, 0.4); }
    }
    
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 50px;
        padding: 4px 12px;
        font-size: 0.7rem;
        color: #10b981;
        font-weight: 600;
    }
    
    .live-dot {
        width: 6px;
        height: 6px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.3); }
    }
    </style>
""", unsafe_allow_html=True)

# =============================
# 3. SUPABASE CONFIG
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
# 4. SESSION STATE
# =============================
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None


# =============================
# 5. AUTH FUNCTIONS
# =============================
def login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.user_email = res.user.email
        st.session_state.user_id = res.user.id
        st.success("✅ Access Granted")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Authentication failed")


def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.user_email = None
    st.session_state.user_id = None
    st.rerun()


user_email = st.session_state.user_email

# =============================
# 6. SIDEBAR — PREMIUM BRANDING
# =============================
with st.sidebar:
    # Brand Header
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">◆</div>
            <div class="sidebar-title">DIGISPHERE</div>
            <div class="sidebar-subtitle">Premium Data Intelligence</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    if not user_email:
        st.markdown("#### 🔐 Secure Access")
        email = st.text_input("Professional Email", placeholder="your@company.com")
        password = st.text_input("Access Key", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("AUTHENTICATE →", use_container_width=True):
            if email and password:
                login(email, password)
            else:
                st.warning("Enter credentials")
    else:
        # User Info Card
        st.markdown(f"""
            <div style="
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.2);
                border-radius: 12px;
                padding: 1rem;
                margin-bottom: 1rem;
            ">
                <div style="color: #10b981; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
                    ✓ Verified Member
                </div>
                <div style="color: #e2e8f0; font-weight: 500; word-break: break-all;">
                    {user_email}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Sign Out", use_container_width=True):
            logout()
    
    # Footer
    st.divider()
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="color: #4a5568; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px;">
                Powered by
            </div>
            <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 500; margin-top: 4px;">
                DIGISPHERELLC LLC
            </div>
            <div style="color: #4a5568; font-size: 0.6rem; margin-top: 2px;">
                Delaware, USA
            </div>
        </div>
    """, unsafe_allow_html=True)

# =============================
# 7. MAIN INTERFACE
# =============================
if user_email:
    # ----- AUTO-UPSERT CUSTOMER -----
    try:
        result = (
            supabase
            .table("customers")
            .select("subscription_status")
            .eq("email", user_email)
            .execute()
        )

        if not result.data:
            supabase.table("customers").insert({
                "email": user_email,
                "subscription_status": "active",
                "created_at": "now()"
            }).execute()
            result = (
                supabase
                .table("customers")
                .select("subscription_status")
                .eq("email", user_email)
                .execute()
            )

        if not result.data or result.data[0]["subscription_status"] != "active":
            st.warning("⚠️ Premium subscription required")
            st.info("📧 Contact: support@digispherellc.com")
            st.stop()

    except Exception as e:
        st.error(f"⚠️ System error: {str(e)}")
        st.stop()

    # ----- HERO HEADER -----
    col_header, col_status = st.columns([4, 1])
    
    with col_header:
        st.markdown('<p class="hero-title">Market Intelligence Hub</p>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">Real-time access to premium talent datasets and market analytics</p>', unsafe_allow_html=True)
    
    with col_status:
        st.markdown("""
            <div style="text-align: right; padding-top: 1rem;">
                <span class="live-indicator">
                    <span class="live-dot"></span>
                    LIVE DATA
                </span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="brand-badge">◆ DIGISPHERELLC — Enterprise Data Solutions</div>', unsafe_allow_html=True)
    
    st.divider()

    # ----- DATASET SELECTION -----
    DATASETS_DIR = "datasets"

    try:
        csv_files = [f for f in os.listdir(DATASETS_DIR) if f.endswith('.csv')]
    except FileNotFoundError:
        st.error(f"Directory not found: '{DATASETS_DIR}'")
        st.stop()

    if not csv_files:
        st.warning(f"No datasets available in '{DATASETS_DIR}'")
        st.stop()

    st.markdown('<div class="section-title">Database Selection</div>', unsafe_allow_html=True)
    selected_dataset = st.selectbox("Choose Intelligence Asset", csv_files, label_visibility="collapsed")

    if selected_dataset:
        dataset_path = os.path.join(DATASETS_DIR, selected_dataset)
        df = pd.read_csv(dataset_path)

        # ----- ANALYTICS OVERVIEW -----
        st.divider()
        
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.metric("Total Records", f"{len(df):,}")
        with m2:
            if 'location' in df.columns:
                st.metric("Regions", f"{df['location'].nunique():,}")
            else:
                st.metric("Columns", f"{len(df.columns):,}")
        with m3:
            if 'company' in df.columns:
                st.metric("Companies", f"{df['company'].nunique():,}")
            else:
                st.metric("Data Points", f"{len(df) * len(df.columns):,}")
        with m4:
            st.metric("Status", "SYNCED ✓")

        st.markdown("<br>", unsafe_allow_html=True)

        # ----- TABS -----
        tab1, tab2, tab3 = st.tabs([
            "◆ Data Explorer",
            "⚡ Power Search", 
            "↓ Export Center"
        ])

        with tab1:
            st.markdown('<div class="section-title">High-Fidelity Data Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(100), use_container_width=True, height=500)
            
            st.markdown(f"""
                <div style="text-align: center; padding: 1rem; color: #64748b; font-size: 0.8rem;">
                    Displaying 100 of {len(df):,} records • Full export available in Export Center
                </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="section-title">Intelligent Search Engine</div>', unsafe_allow_html=True)
            
            search_query = st.text_input(
                "Search", 
                placeholder="Search by skill, location, company, name...",
                label_visibility="collapsed"
            )
            
            if search_query:
                import re
                sanitized_query = re.escape(search_query.strip())
                if len(sanitized_query) > 100:
                    st.warning("Query too long")
                else:
                    mask = df.astype(str).apply(
                        lambda row: row.str.contains(sanitized_query, case=False, regex=True).any(), 
                        axis=1
                    )
                    filtered_df = df[mask]
                    
                    st.markdown(f"""
                        <div style="
                            background: rgba(124, 58, 237, 0.1);
                            border: 1px solid rgba(124, 58, 237, 0.2);
                            border-radius: 10px;
                            padding: 0.75rem 1rem;
                            margin-bottom: 1rem;
                            color: #c4b5fd;
                            font-size: 0.85rem;
                        ">
                            Found <strong>{len(filtered_df):,}</strong> matching records for "<strong>{search_query}</strong>"
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.dataframe(filtered_df, use_container_width=True, height=450)
            else:
                st.markdown("""
                    <div style="
                        text-align: center;
                        padding: 3rem;
                        color: #64748b;
                    ">
                        <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔍</div>
                        <div>Enter a search term to filter the dataset</div>
                        <div style="font-size: 0.8rem; margin-top: 0.5rem;">
                            Try: Python, London, Senior, Engineer...
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="section-title">Data Export</div>', unsafe_allow_html=True)
            
            st.markdown("""
                <div style="
                    text-align: center;
                    padding: 2rem;
                    background: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(168, 139, 250, 0.1);
                    border-radius: 16px;
                    margin-bottom: 1.5rem;
                ">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
                    <div style="color: #e2e8f0; font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;">
                        Complete Dataset Package
                    </div>
                    <div style="color: #64748b; font-size: 0.9rem;">
                        Full data export with all columns and records
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            col_dl = st.columns([1, 2, 1])[1]
            with col_dl:
                st.download_button(
                    label=f"⬇ DOWNLOAD {selected_dataset.upper()}",
                    data=df.to_csv(index=False),
                    file_name=f"DIGISPHERE_{selected_dataset}",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.markdown("""
                <div style="text-align: center; padding: 1rem; color: #64748b; font-size: 0.75rem;">
                    ✓ Excel & Google Sheets compatible • ✓ UTF-8 Encoded • ✓ Production Ready
                </div>
            """, unsafe_allow_html=True)

else:
    # =============================
    # LANDING PAGE — 2 COLUMNS LAYOUT
    # LEFT: Login Form | RIGHT: Hero + Features
    # =============================
    
    # Main 2-column layout
    col_login, col_spacer, col_content = st.columns([1.2, 0.2, 2.5])
    
    # ===== LEFT COLUMN: LOGIN FORM =====
    with col_login:
        # Brand
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0 2rem 0;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">◆</div>
                <div style="
                    font-family: 'Inter', sans-serif;
                    font-size: 1.2rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    letter-spacing: 3px;
                ">DIGISPHERE</div>
                <div style="color: #4a5568; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px;">
                    Premium Data Intelligence
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Login Card
        st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(168, 139, 250, 0.15);
                border-radius: 20px;
                padding: 2rem;
            ">
                <div style="
                    color: #a78bfa;
                    font-size: 0.75rem;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    font-weight: 600;
                    margin-bottom: 1.5rem;
                    text-align: center;
                ">🔐 Secure Access</div>
        """, unsafe_allow_html=True)
        
        main_email = st.text_input("Professional Email", placeholder="your@company.com", key="main_email", label_visibility="collapsed")
        main_password = st.text_input("Access Key", type="password", placeholder="Password", key="main_password", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("ACCESS DASHBOARD →", use_container_width=True, key="main_login_btn"):
            if main_email and main_password:
                try:
                    res = supabase.auth.sign_in_with_password({
                        "email": main_email,
                        "password": main_password
                    })
                    st.session_state.user_email = res.user.email
                    st.session_state.user_id = res.user.id
                    st.success("✅ Access Granted")
                    st.rerun()
                except Exception as e:
                    st.error("❌ Invalid credentials")
            else:
                st.warning("Enter email and password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
            <div style="text-align: center; padding: 2rem 0 0 0;">
                <div style="color: #4a5568; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px;">
                    Powered by
                </div>
                <div style="color: #64748b; font-size: 0.7rem; font-weight: 500; margin-top: 4px;">
                    DIGISPHERELLC LLC
                </div>
                <div style="color: #4a5568; font-size: 0.55rem; margin-top: 2px;">
                    Delaware, USA
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # ===== RIGHT COLUMN: HERO + FEATURES =====
    with col_content:
        # Hero Title
        st.markdown("""
            <div style="padding: 0 0 1.5rem 0;">
                <h1 style="
                    font-family: 'Inter', sans-serif;
                    font-size: 3rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #c4b5fd 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 0.75rem;
                    line-height: 1.1;
                ">Premium Data<br>Intelligence</h1>
                <p style="color: #94a3b8; font-size: 1rem; line-height: 1.7; max-width: 500px;">
                    Access exclusive market datasets curated for enterprise recruiters, 
                    research teams, and data-driven organizations worldwide.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature Cards - 3 columns inside the right column
        fc1, fc2, fc3 = st.columns(3)
        
        with fc1:
            st.markdown("""
                <div style="
                    background: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(168, 139, 250, 0.12);
                    border-radius: 14px;
                    padding: 1.25rem 1rem;
                    text-align: center;
                ">
                    <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🎯</div>
                    <div style="color: #e2e8f0; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.25rem;">Curated Datasets</div>
                    <div style="color: #64748b; font-size: 0.75rem;">Premium talent pools</div>
                </div>
            """, unsafe_allow_html=True)
        
        with fc2:
            st.markdown("""
                <div style="
                    background: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(168, 139, 250, 0.12);
                    border-radius: 14px;
                    padding: 1.25rem 1rem;
                    text-align: center;
                ">
                    <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">⚡</div>
                    <div style="color: #e2e8f0; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.25rem;">Real-Time Updates</div>
                    <div style="color: #64748b; font-size: 0.75rem;">Fresh data synced</div>
                </div>
            """, unsafe_allow_html=True)
        
        with fc3:
            st.markdown("""
                <div style="
                    background: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(168, 139, 250, 0.12);
                    border-radius: 14px;
                    padding: 1.25rem 1rem;
                    text-align: center;
                ">
                    <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🔐</div>
                    <div style="color: #e2e8f0; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.25rem;">Enterprise Security</div>
                    <div style="color: #64748b; font-size: 0.75rem;">SOC2 compliant</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Stats or testimonial area
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="
                background: rgba(124, 58, 237, 0.08);
                border: 1px solid rgba(168, 139, 250, 0.15);
                border-radius: 12px;
                padding: 1rem 1.5rem;
                display: flex;
                gap: 2rem;
            ">
                <div style="text-align: center; flex: 1;">
                    <div style="color: #a78bfa; font-size: 1.5rem; font-weight: 700;">50K+</div>
                    <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase;">Profiles</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="color: #a78bfa; font-size: 1.5rem; font-weight: 700;">120+</div>
                    <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase;">Countries</div>
                </div>
                <div style="text-align: center; flex: 1;">
                    <div style="color: #a78bfa; font-size: 1.5rem; font-weight: 700;">99.9%</div>
                    <div style="color: #64748b; font-size: 0.7rem; text-transform: uppercase;">Uptime</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


