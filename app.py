import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE ---
# Incolla qui il tuo ULTIMO link di SheetDB
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Aggiungiamo un timestamp per avere dati sempre freschi
        r = requests.get(f"{API_URL}?t={datetime.now().timestamp()}", timeout=10)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza'])
    except:
        return pd.DataFrame()

def aggiungi_utente(email, password):
    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    
    # I nomi in questa lista devono essere IDENTICI a quelli della riga 1 dell'Excel
    nuovo_dato = {
        "email": str(email).strip(),
        "password": str(password).strip(),
        "nome": "Mamma",
        "bimbo": "---",
        "taglia": "---",
        "inizio": datetime.now().strftime("%Y-%m-%d"),
        "scadenza": scad
    }
    
    headers = {"Content-Type": "application/json"}
    payload = {"data": [nuovo_dato]}
    
    try:
        res = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        return res.status_code, res.text
    except Exception as e:
        return 500, str(e)

# --- 2. CONFIGURAZIONE APP ---
st.set_page_config(page_title="LoopBaby", layout="centered")
if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; border-radius: 0 0 30px 30px; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; height: 50px; border: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df_globale = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty:
                        m = df_globale[(df_globale['email'].astype(str).str.lower() == e.lower()) & (df_globale['password'].astype(str) == str(p))]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
        with t2:
            with st.form("r"):
                er, pr = st.text_input("Email"), st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    status, text = aggiungi_utente(er, pr)
                    if status == 201:
                        st.success("✅ REGISTRATO! Ora puoi accedere.")
                        st.balloons()
                    else:
                        st.error(f"ERRORE {status}: Il database dice '{text}'")
                        st.info("💡 Suggerimento: Assicurati che le colonne dell'Excel siano: email, password, nome, bimbo, taglia, inizio, scadenza")
else:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown(f"### Ciao {st.session_state.user.get('nome', 'Mamma')}! 👋")
    if st.button("Logout"): 
        st.session_state.user = None
        vai("Welcome")
