import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import json

# --- 1. CONFIGURAZIONE ---
API_URL = "https://sheetdb.io"

def carica_db_chirurgico():
    try:
        # Usiamo un parametro casuale per distruggere la cache di SheetDB
        res = requests.get(f"{API_URL}?t={datetime.now().microsecond}", timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                # Pulizia nomi colonne: togliamo spazi e rendiamo tutto minuscolo
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df, data
        return pd.DataFrame(), []
    except:
        return pd.DataFrame(), []

def aggiungi_utente(nuovo):
    return requests.post(API_URL, json={"data": [nuovo]}, timeout=15).status_code

# --- 2. SETUP PAGINA ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# --- 3. DIAGNOSI (VEDI COSA LEGGE L'APP) ---
df_globale, raw_data = carica_db_chirurgico()

with st.expander("🔍 DIAGNOSI DATABASE (Solo per Manuel)"):
    st.write("Cosa vede l'app in questo momento:")
    st.json(raw_data)
    if not df_globale.empty:
        st.write("Colonne trovate:", list(df_globale.columns))

# --- 4. LOGICA ACCESSO ---
st.title("👶 LOOPBABY")

if st.session_state.user is None:
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t1:
        e = st.text_input("Email").strip().lower()
        p = st.text_input("Password", type="password").strip()
        
        if st.form_submit_button if False else st.button("ENTRA"):
            if not df_globale.empty:
                # Confronto ultra-flessibile per evitare errori di Excel
                df_globale['email_check'] = df_globale['email'].astype(str).str.strip().str.lower()
                df_globale['pass_check'] = df_globale['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                
                match = df_globale[(df_globale['email_check'] == e) & (df_globale['pass_check'] == p)]
                
                if not match.empty:
                    st.session_state.user = match.iloc[-1].to_dict()
                    st.success("Accesso riuscito!")
                    vai("Home")
                else:
                    st.error("Credenziali non trovate nel database.")
            else:
                st.warning("Il database sembra ancora vuoto per l'app. Clicca 'Aggiorna' o Registrati.")

        if st.button("🔄 AGGIORNA DATI"):
            st.rerun()

    with t2:
        with st.form("r"):
            er = st.text_input("Email")
            pr = st.text_input("Scegli Password")
            if st.form_submit_button("CREA ACCOUNT"):
                scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                nuovo = {"email": er.strip(), "password": pr.strip(), "nome genitore": "Mamma", "taglia": "---", "scadenza": scad}
                if aggiungi_utente(nuovo) == 201:
                    st.success("✅ REGISTRATO! Aspetta 3 secondi e prova ad accedere.")
                    st.balloons()
else:
    st.write(f"### Ciao {st.session_state.user.get('nome genitore', 'Mamma')}! 👋")
    if st.button("Logout"): 
        st.session_state.user = None
        vai("Welcome")
