import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (CON SUPER-REFRESH) ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Usiamo un timestamp al secondo per distruggere ogni cache possibile
        t = datetime.now().strftime('%H%M%S')
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            dati = res.json()
            if dati and isinstance(dati, list) and len(dati) > 0:
                df = pd.DataFrame(dati)
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        # Se il database risponde vuoto, restituiamo una struttura base per non bloccare l'app
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])
    except:
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])

def aggiungi_utente(nuovo):
    return requests.post(API_URL, json={"data": [nuovo]}, timeout=15).status_code

def aggiorna_utente(email, dati):
    return requests.patch(f"{API_URL}/email/{email}", json={"data": dati}).status_code

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")
if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

img_data, logo_bg = "", "" # Qui andrebbero le tue funzioni get_base64

# --- 3. LOGICA ---
df_globale = carica_db()

if st.session_state.user is None:
    st.title("👶 LOOPBABY")
    
    if st.session_state.pagina == "Welcome":
        st.write("L'armadio circolare che cresce con il tuo bambino.")
        if st.button("INIZIA ORA"): vai("Login")
    
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty and 'email' in df_globale.columns:
                        # Pulizia password per Excel
                        df_globale['p_c'] = df_globale['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        m = df_globale[(df_globale['email'].str.lower() == e) & (df_globale['p_c'] == p)]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati.")
                    else:
                        st.error("Il sistema non vede ancora utenti registrati. Clicca il tasto Refresh sotto.")
            
            if st.button("🔄 AGGIORNA E RIPROVA"): st.rerun()

        with t2:
            with st.form("r"):
                er = st.text_input("Tua migliore Email")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                    nuovo = {"email": er.strip(), "password": pr.strip(), "nome": "Mamma", "bimbo": "---", "taglia": "---", "inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad, "locker": "Da impostare"}
                    if aggiungi_utente(nuovo) == 201:
                        st.success("✅ REGISTRATA! Aspetta 5 secondi e clicca su 'AGGIORNA' per accedere.")
                        st.balloons()
else:
    st.markdown(f"## Ciao {st.session_state.user.get('nome', 'Mamma')}! 👋")
    st.write("Sei dentro! Il database funziona.")
    if st.button("Logout"): 
        st.session_state.user = None
        vai("Welcome")
