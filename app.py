import streamlit as st
import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# Configuration de la page EN PREMIER
st.set_page_config(page_title="TalentIQ AI", layout="wide")

# Utilisation de os.environ pour Elestio (plus fiable que st.secrets ici)
SUPABASE_URL = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY") or st.secrets.get("SUPABASE_ANON_KEY", "")

@st.cache_resource
def init_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("⚠️ Variables SUPABASE_URL ou SUPABASE_ANON_KEY manquantes dans Elestio Settings > ENV Vars")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# === SESSION CHECK ===
def get_current_user():
    try:
        res = supabase.auth.get_user()
        return res.user
    except:
        return None

user = get_current_user()

# === SIDEBAR AUTH ===
with st.sidebar:
    st.title("🔐 TalentIQ")
    if not user:
        st.subheader("Sign In")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            try:
                supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.rerun()
            except Exception as e:
                st.error(f"Login failed: {e}")
    else:
        st.success(f"✅ {user.email}")
        if st.button("🚪 Logout", use_container_width=True):
            supabase.auth.sign_out()
            st.rerun()

# === MAIN LOGIC ===
if user:
    # Vérification abonnement (Table customers)
    try:
        customer = supabase.table("customers").select("subscription_status").eq("email", user.email).execute()
        if not customer.data or customer.data[0]["subscription_status"] != "active":
            st.warning("❌ Abonnement requis pour accéder aux données.")
            st.stop()
    except Exception as e:
        st.info("Configuration de la table 'customers' en cours...")

    st.title("🎯 TalentIQ Premium Dashboard")
    st.caption("DIGISPHERELLC LLC - Intelligence Marché")
    
    # Chargement du Dataset
    csv_file = "premium_architects.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Search", "📤 Export"])
        
        with tab1:
            st.metric("Total Profiles", len(df))
            st.dataframe(df.head(50), use_container_width=True)
            
        with tab2:
            search = st.text_input("Filtrer par nom, techno ou ville...")
            if search:
                filtered = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False).any(), axis=1)]
                st.dataframe(filtered)
                
        with tab3:
            st.download_button("📥 Télécharger le CSV complet", df.to_csv(index=False), "export_talentiq.csv")
    else:
        st.error(f"Fichier {csv_file} introuvable à la racine du projet.")
else:
    st.header("Bienvenue sur TalentIQ")
    st.info("Veuillez vous connecter via la barre latérale pour accéder aux datasets premium.")
