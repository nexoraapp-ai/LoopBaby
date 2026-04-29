import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        r = requests.get(f"{API_URL}?t={datetime.now().timestamp()}", timeout=10)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])
    except: return pd.DataFrame()

def aggiungi_utente(email, password):
    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    # I nomi qui sotto devono essere IDENTICI alle colonne dell'Excel
    nuovo_dato = {
        "email": str(email).strip(),
        "password": str(password).strip(),
        "nome": "Mamma",
        "bimbo": "---",
        "taglia": "---",
        "inizio": datetime.now().strftime("%Y-%m-%d"),
        "scadenza": scad,
        "locker": "Da definire"
    }
    # Headers di sicurezza per evitare l'errore 405
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        res = requests.post(API_URL, json={"data": [nuovo_dato]}, headers=headers, timeout=15)
        return res.status_code
    except: return 500

# --- 2. CONFIGURAZIONE APP ---
st.set_page_config(page_title="LoopBaby", layout="centered")
if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# --- 3. INTERFACCIA ---
st.title("👶 LOOPBABY")

df_globale = carica_db()

if st.session_state.user is None:
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("login"):
            e, p = st.text_input("Email"), st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                if not df_globale.empty and 'email' in df_globale.columns:
                    m = df_globale[(df_globale['email'].astype(str).str.lower() == e.lower()) & (df_globale['password'].astype(str) == str(p))]
                    if not m.empty:
                        st.session_state.user = m.iloc[-1].to_dict()
                        vai("Home")
                    else: st.error("Dati errati")
    with t2:
        with st.form("reg"):
            er, pr = st.text_input("Email "), st.text_input("Scegli Password")
            if st.form_submit_button("CREA ACCOUNT"):
                status = aggiungi_utente(er, pr)
                if status == 201:
                    st.success("✅ REGISTRATO! Ora puoi accedere.")
                    st.balloons()
                else:
                    st.error(f"ERRORE {status}: SheetDB ha rifiutato la scrittura. Verifica di aver premuto SAVE nelle impostazioni di SheetDB.io")
else:
    st.write(f"### Ciao {st.session_state.user.get('nome', 'Mamma')}! 👋")
    if st.button("Logout"): 
        st.session_state.user = None
        vai("Welcome")
