import streamlit as st
import requests
import json
import base64
import os
from datetime import datetime, timedelta

# --- 1. CONNESSIONE DIRETTA (ADDIO 404) ---
URL_DB = "https://supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

HEADERS = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

# --- 2. FUNZIONI DI ACCESSO ---
def login_diretto(email, password):
    payload = {"email": email, "password": password}
    res = requests.post(f"{URL_DB}/token?grant_type=password", json=payload, headers=HEADERS)
    if res.status_code == 200:
        st.session_state.user = res.json()["user"]
        st.session_state.pagina = "Home"
        st.rerun()
    else:
        st.error("Credenziali errate o email non confermata.")

def registra_diretto(email, password):
    payload = {"email": email, "password": password}
    res = requests.post(f"{URL_DB}/signup", json=payload, headers=HEADERS)
    if res.status_code == 200:
        st.success("📩 REGISTRAZIONE AVVENUTA! Controlla la mail (e lo spam) per attivare l'account.")
    else:
        st.error(f"Errore: {res.json().get('msg', 'Riprova più tardi')}")

# --- 3. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# --- 4. CSS ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #FDFBF7; max-width: 450px; margin: 0 auto; }
    div.stButton > button { background-color: #f43f5e !important; color: white !important; border-radius: 20px !important; width: 100% !important; border: none !important; font-weight: bold; }
    .card { border-radius: 20px; padding: 20px; background: white; border: 1px solid #EAE2D6; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. PAGINE ---
if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;'>👶 LOOPBABY</h1>", unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<div class='card' style='text-align:center;'><h3>L'armadio circolare che cresce con il tuo bambino 🔄</h3></div>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    
    elif st.session_state.pagina == "Login":
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"): login_diretto(e, p)
        with t2:
            with st.form("r"):
                er = st.text_input("La tua migliore Email")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"): registra_diretto(er, pr)
else:
    # --- HOME ---
    st.title("Home 👶")
    st.write(f"Benvenuta, {st.session_state.user['email']}")
    if st.button("Logout"):
        st.session_state.user = None
        vai("Welcome")
