import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE ---
API_URL = "https://sheetdb.io"

def carica_db_forzato():
    try:
        # Usiamo un parametro casuale unico ogni volta per distruggere la cache
        cache_buster = datetime.now().strftime("%Y%m%d%H%M%S")
        res = requests.get(f"{API_URL}?t={cache_buster}", timeout=10)
        if res.status_code == 200:
            dati = res.json()
            if dati and len(dati) > 0:
                df = pd.DataFrame(dati)
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def aggiungi_utente(nuovo):
    return requests.post(API_URL, json={"data": [nuovo]}, timeout=15).status_code

# --- 2. SETUP ---
st.set_page_config(page_title="LoopBaby", layout="centered")
if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

img_data, logo_bg = "", "" # Inserisci qui le tue funzioni get_base64 se le hai

# --- 3. LOGICA ---
df_globale = carica_db_forzato()

if st.session_state.user is None:
    st.title("👶 LOOPBABY")
    
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t1:
        e = st.text_input("Email").strip().lower()
        p = st.text_input("Password", type="password").strip()
        
        if st.button("ENTRA"):
            if not df_globale.empty:
                # Pulizia chirurgica dei dati
                df_globale['email_c'] = df_globale['email'].astype(str).str.strip().str.lower()
                df_globale['pass_c'] = df_globale['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                
                user_match = df_globale[(df_globale['email_c'] == e) & (df_globale['pass_c'] == p)]
                
                if not user_match.empty:
                    st.session_state.user = user_match.iloc[-1].to_dict()
                    st.success("Accesso eseguito!")
                    vai("Home")
                else:
                    st.error("Credenziali errate. Riprova.")
            else:
                st.warning("Il database non vede ancora utenti. Clicca il tasto sotto o Registrati.")
                if st.button("🔄 FORZA AGGIORNAMENTO DATI"):
                    st.rerun()

    with t2:
        er = st.text_input("La tua migliore Email")
        pr = st.text_input("Scegli Password")
        if st.button("CREA ACCOUNT"):
            scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
            nuovo = {"email": er.strip(), "password": pr.strip(), "nome": "Mamma", "bimbo": "---", "taglia": "---", "inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad, "locker": "Non impostato"}
            if aggiungi_utente(nuovo) == 201:
                st.success("✅ REGISTRATO! Ora aspetta 10 secondi e prova ad accedere.")
                st.balloons()
else:
    st.markdown(f"## Ciao {st.session_state.user.get('nome', 'Mamma')}! 👋")
    if st.button("Esci"): 
        st.session_state.user = None
        st.rerun()
