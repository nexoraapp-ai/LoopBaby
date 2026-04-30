import streamlit as st
import os
import base64
import json
import requests
from datetime import date, datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE (SHEETDB) ---
SHEETDB_URL = "https://sheetdb.io"

def registra_utente(email, password, nome, bimbo, taglia, locker):
    payload = {"data": [{
        "email": email.strip().lower(),
        "password": password,
        "nome_genitore": nome,
        "nome_bambino": bimbo,
        "taglia": taglia,
        "data_inizio": str(date.today()),
        "scadenza": str(date.today() + timedelta(days=90)),
        "locker": locker
    }]}
    r = requests.post(SHEETDB_URL, json=payload, headers={"Content-Type": "application/json"})
    return r.status_code

def login(email, password):
    try:
        t = datetime.now().microsecond
        r = requests.get(f"{SHEETDB_URL}?t={t}")
        utenti = r.json()
        for u in utenti:
            if str(u.get("email")).strip().lower() == email.strip().lower() and str(u.get("password")) == str(password):
                return u
    except: pass
    return None

# --- 2. STATO APP ---
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")
if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi(n, p):
    st.session_state.carrello.append({"nome": n, "prezzo": p})
    st.toast(f"✅ {n} aggiunto!")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS TOTALE (Full Design 23:30) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; height: 48px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN / REGISTER ---
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("l"):
            e, p = st.text_input("Email"), st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                u = login(e, p)
                if u: st.session_state.loggato, st.session_state.user_data = True, u; st.rerun()
                else: st.error("Dati errati")
    with t2:
        with st.form("r"):
            re, rp = st.text_input("Email"), st.text_input("Scegli Password")
            rn, rb = st.text_input("Tuo Nome"), st.text_input("Nome Bambino")
            rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste"])
            if st.form_submit_button("CREA ACCOUNT"):
                if registra_utente(re, rp, rn, rb, rt, rl) == 201: st.success("Registrato! Accedi ora.")
    st.stop()
