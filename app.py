import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        res = requests.get(f"{API_URL}?t={datetime.now().timestamp()}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza'])
    except: return pd.DataFrame()

def aggiungi_utente(nuovo):
    # Fix per errore 405: forziamo il formato JSON e gli headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = json.dumps({"data": [nuovo]})
    res = requests.post(API_URL, data=payload, headers=headers, timeout=15)
    return res

# --- 2. CONFIGURAZIONE ---
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

# --- 3. CSS PROFESSIONALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df.empty and 'email' in df.columns:
                        match = df[(df['email'].str.lower() == e.lower()) & (df['password'].astype(str) == str(p))]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
                    else: st.error("Database in aggiornamento...")
        with t2:
            with st.form("r"):
                er, pr = st.text_input("Tua Email"), st.text_input("Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                    nuovo = {"email": er, "password": str(pr), "nome": "Mamma", "bimbo": "---", "taglia": "---", "inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad}
                    res = aggiungi_utente(nuovo)
                    if res.status_code == 201:
                        st.success("✅ REGISTRATO! Ora puoi accedere.")
                    else:
                        st.error(f"Errore {res.status_code}. Controlla di aver premuto SAVE su SheetDB.")
else:
    # --- HOME ---
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    nome = st.session_state.user.get('nome', 'Mamma')
    st.markdown(f"### Ciao {nome}! 👋")
    if img_data: st.markdown(f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">', unsafe_allow_html=True)
    if st.button("Esci"): st.session_state.user = None; vai("Welcome")

    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📖", "Info"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag)
