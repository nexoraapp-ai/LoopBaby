import streamlit as st
from supabase import create_client, Client
import base64
import os

# --- 1. CONNESSIONE SUPABASE (FIX 404 FORZATO) ---
URL_PROGETTO = "https://supabase.co"
CHIAVE_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def get_supabase_client():
    # Il segreto è passare l'URL anche nelle opzioni di autenticazione
    return create_client(
        URL_PROGETTO, 
        CHIAVE_ANON
    )

supabase: Client = get_supabase_client()

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "dati" not in st.session_state: st.session_state.dati = {}

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# --- 3. LOGICA ACCOUNT ---
def login(e, p):
    try:
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        prof = supabase.table("profili").select("*").eq("id", res.user.id).execute()
        st.session_state.dati = prof.data[0] if prof.data else {}
        vai("Home")
    except: st.error("Email o Password errati.")

def registro(e, p):
    try:
        # Questo comando ora punterà correttamente al TUO progetto
        res = supabase.auth.sign_up({"email": e, "password": p})
        if res.user:
            # Crea subito il profilo per evitare il 404 futuro
            supabase.table("profili").upsert({"id": res.user.id, "nome_genitore": "Nuova Mamma"}).execute()
            st.success("📩 Account creato! Ora puoi accedere.")
    except Exception as err:
        st.error(f"Errore tecnico: {err}")

# --- 4. CSS ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #FDFBF7; max-width: 450px; margin: 0 auto; }
    div.stButton > button { background-color: #f43f5e !important; color: white !important; border-radius: 20px !important; width: 100% !important; border: none !important; }
    .card { border-radius: 20px; padding: 20px; background: white; border: 1px solid #EAE2D6; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. PAGINE ---
if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;'>👶 LOOPBABY</h1>", unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<div class='card' style='text-align:center;'><h3>L'armadio circolare che cresce con il tuo bambino</h3></div>", unsafe_allow_html=True)
        if st.button("INIZIA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            e = st.text_input("Email", key="l_e")
            p = st.text_input("Password", type="password", key="l_p")
            if st.button("ENTRA"): login(e, p)
        with t2:
            er = st.text_input("La tua migliore Email", key="r_e")
            pr = st.text_input("Scegli Password", type="password", key="r_p")
            if st.button("CREA ACCOUNT"): registro(er, pr)
else:
    # Navigazione superiore
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🏠"): vai("Home")
    with c2: 
        if st.button("👤"): vai("Profilo")
    with c3:
        if st.button("🚪"): 
            supabase.auth.sign_out()
            st.session_state.user = None
            vai("Welcome")

    if st.session_state.pagina == "Home":
        n = st.session_state.dati.get("nome_genitore", "Mamma")
        st.markdown(f"## Ciao {n}! 👋")
        st.markdown("<div class='card'>Benvenuta nel giro infinito di LoopBaby.</div>", unsafe_allow_html=True)

    elif st.session_state.pagina == "Profilo":
        st.title("Tuo Profilo 👤")
        with st.form("p"):
            nome = st.text_input("Tuo Nome", st.session_state.dati.get("nome_genitore",""))
            if st.form_submit_button("SALVA"):
                supabase.table("profili").upsert({"id": st.session_state.user.id, "nome_genitore": nome}).execute()
                st.session_state.dati["nome_genitore"] = nome
                st.success("Salvato online!")
