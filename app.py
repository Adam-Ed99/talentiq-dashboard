import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client

# =============================
# 1. PAGE CONFIG (TOUJOURS EN PREMIER)
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
    if not SUPABASE_URL or not SUPABASE_KEY:
        st.error("❌ Supabase secrets missing. Check Streamlit Cloud settings.")
        st.stop()
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# =============================
# 3. GESTION DU RESET MOT DE PASSE (RECOVERY)
# =============================
# Ce bloc intercepte le lien envoyé par Supabase
query_params = st.query_params
if "type" in query_params and query_params["type"] == "recovery":
    st.title("🔄 Reset your password")
    st.info("Please enter your new password below.")
    
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    if st.button("Update Password"):
        if new_password == confirm_password and len(new_password) >= 6:
            try:
                supabase.auth.update_user({"password": new_password})
                st.success("✅ Password updated! You can now login from the sidebar.")
                # On nettoie l'URL pour sortir du mode recovery
                st.query_params.clear()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Passwords do not match or are too short (min 6 chars).")
    st.stop() # Arrête l'exécution pour ne pas afficher le reste de l'app

# =============================
# 4. SESSION STATE & AUTH FUNCTIONS
# =============================
if "user_email" not in st.session_state:
    st.session_state.user_email = None

def login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user_email = res.user.email
        st.success("✅ Login successful!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Login failed: {str(e)}")

def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.user_email = None
    st.rerun()

# =============================
# 5. SIDEBAR UI
# =============================
with st.sidebar:
    st.title("🔐 TalentIQ")
    if not st.session_state.user_email:
        st.subheader("Sign in")
        email_input = st.text_input("Email")
        pass_input = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            login(email_input, pass_input)
        
        # Optionnel : Lien pour déclencher l'envoi d'un mail de reset
        if st.button("Forgot password?"):
            if email_input:
                supabase.auth.reset_password_for_email(email_input)
                st.info("Reset link sent to your email!")
            else:
                st.warning("Enter your email first.")
    else:
        st.success(f"Logged in as: {st.session_state.user_email}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()

# =============================
# 6. MAIN APP LOGIC
# =============================
user_email = st.session_state.user_email

if user_email:
    # ----- VÉRIFICATION ABONNEMENT (Basé sur ta table customers) -----
    try:
        # On vérifie si l'email est bien marqué comme 'active'
        result = supabase.table("customers").select("subscription_status").eq("email", user_email).execute()

        if not result.data or result.data[0]["subscription_status"] != "active":
            st.warning("❌ Active subscription required.")
            st.info("Contact support@digispherellc.com to activate your subscription.")
            st.stop()
    except Exception as e:
        st.error(f"⚠️ Subscription check failed: {str(e)}")
        st.stop()

    # ----- DASHBOARD PREMIUM -----
    st.title("🎯 TalentIQ Premium Dashboard")

    # Calcul du chemin ABSOLU pour le dossier datasets
    base_path = os.path.dirname(os.path.abspath(__file__))
    DATASETS_DIR = os.path.join(base_path, "datasets")

    # Scan des fichiers CSV
    if os.path.exists(DATASETS_DIR):
        csv_files = [f for f in os.listdir(DATASETS_DIR) if f.endswith('.csv')]
        
        if not csv_files:
            st.warning(f"No CSV datasets found in '{DATASETS_DIR}'.")
        else:
            selected_dataset = st.selectbox("Select a Dataset:", csv_files)
            if selected_dataset:
                dataset_path = os.path.join(DATASETS_DIR, selected_dataset)
                df = pd.read_csv(dataset_path)

                tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Search", "📤 Export"])
                with tab1:
                    st.metric("Total Profiles", len(df))
                    st.dataframe(df.head(50), use_container_width=True)
                with tab2:
                    query = st.text_input("Search (name, skill, city...)")
                    if query:
                        filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(query, case=False).any(), axis=1)]
                        st.dataframe(filtered_df, use_container_width=True)
                with tab3:
                    st.download_button("📥 Download CSV", df.to_csv(index=False), file_name=selected_dataset, mime="text/csv")
    else:
        # Message d'aide si le dossier est toujours introuvable
        st.error(f"❌ Folder '{DATASETS_DIR}' not found.")
        st.write("Current directory content:", os.listdir(base_path))

else:
    st.title("👋 Welcome to TalentIQ")
    st.info("Please sign in from the sidebar to access your premium data.")
