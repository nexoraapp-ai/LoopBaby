import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE (IL TUO MOTORE)
# ==========================================
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except: return pd.DataFrame()

def registra_utente(email, password, nome="", bimbo="", taglia="50-56 cm", locker=""):
    payload = {
        "data": [{
            "email": email.strip().lower(),
            "password": password,
            "nome_genitore": nome,
            "nome_bambino": bimbo,
            "taglia": taglia,
            "data_inizio": str(date.today()),
            "scadenza": str(date.today() + timedelta(days=90)),
            "locker": locker
        }]
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(API_URL, json=payload, headers=headers)
    return r.status_code

def login(email, password):
    try:
        r = requests.get(API_URL)
        utenti = r.json()
        for u in utenti:
            if str(u.get("email")).strip().lower() == email.strip().lower() and str(u.get("password")) == str(password):
                return u
    except: pass
    return None

# ==========================================
# 2. CONFIGURAZIONE PAGINA & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# ==========================================
# 3. CSS INTEGRALE (IL TUO DESIGN 23:30)
# ==========================================
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 140px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 40px 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    }}
    .header-text {{ color: white; font-size: 34px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 10px rgba(0,0,0,0.3); text-transform: uppercase; }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 22px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 50px; font-size: 16px; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.2);
    }}

    .card {{ border-radius: 28px; padding: 22px; margin: 10px 15px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 12px 30px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #1e293b !important; border: none !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .prezzo-rosa {{ color: #ec4899; font-size: 26px; font-weight: 900; margin-top: 10px; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 18px; background: #FFFFFF; border-radius: 20px; margin-bottom: 15px; border-left: 6px solid #f43f5e; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)
