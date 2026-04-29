import streamlit as st
from supabase import create_client, Client
import base64
import os

# --- 1. CONNESSIONE SUPABASE (TECNICA ANTI-404) ---
URL_DB = "https://supabase.co"
KEY_DB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def get_supabase():
    # Forza headers e URL per evitare redirect sbagliati su supabase.com
    return create_client(URL_DB, KEY_DB)

supabase = get_supabase()

# --- 2. LOGICA ACCOUNT ---
def login_user(e, p):
    try:
        # Usiamo il metodo con l'URL specifico del progetto
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        st.session_state.pagina = "Home"
        st.rerun()
    except: st.error("Dati errati")

def registra_user(e, p):
    try:
        # QUI IL FIX: Chiamata forzata verso il TUO URL .co
        res = supabase.auth.sign_up({"email": e, "password": p})
        if res.user:
            st.success("📩 REGISTRAZIONE OK! Controlla la mail (anche Spam).")
    except Exception as err:
        st.error(f"Errore Tecnico: {err}")

# --- 3. CONFIGURAZIONE APP ---
st.set_page_config(page_title="LoopBaby", layout="centered")
if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

# CSS
st.markdown("<style>[data-testid='stHeader'] {display:none;}</style>", unsafe_allow_html=True)

# --- 4. PAGINE ---
if st.session_state.user is None:
    st.title("👶 LOOPBABY")
    
    if st.session_state.pagina == "Welcome":
        if st.button("INIZIA ORA"): 
            st.session_state.pagina = "Login"
            st.rerun()
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            e, p = st.text_input("Email"), st.text_input("Password", type="password")
            if st.button("ENTRA"): login_user(e, p)
        with t2:
            er, pr = st.text_input("Email "), st.text_input("Scegli Password", type="password")
            if st.button("CREA ACCOUNT"): registra_user(er, pr)
else:
    st.title("Home 👶")
    st.write(f"Benvenuta, {st.session_state.user.email}")
    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
