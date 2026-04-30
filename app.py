import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE & SICUREZZA
# ==========================================
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Cache buster per caricare i dati istantaneamente senza ritardi
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                # Normalizziamo i nomi delle colonne per sicurezza
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except:
        return pd.DataFrame()

def registra_user(dati):
    # Salva i dati reali su Google Sheets via SheetDB
    requests.post(API_URL, json={"data": [dati]})

def hash_password(password):
    # Protezione delle password nell'Excel
    return hashlib.sha256(str.encode(password)).hexdigest()

# ==========================================
# 2. CONFIGURAZIONE PAGINA & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# ==========================================
# 3. CSS PROFESSIONALE (LOOK INTEGRALE 23:30)
# ==========================================
st.markdown(f"""
    <style>
    /* Rimozione elementi nativi Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    
    /* Font Lexend e Sfondo */
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}

    /* Header Custom con Logo */
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 140px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 40px 40px; box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; text-shadow: 2px 2px 10px rgba(0,0,0,0.3); }}

    /* Bottoni Rosa LoopBaby */
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 22px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 52px; font-size: 16px; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
    }}

    /* Card Prodotto e Info */
    .card {{ border-radius: 30px; padding: 25px; margin: 10px 15px; border: 1px solid #EAE2D6; background-color: #FFFFFF; box-shadow: 0 12px 35px rgba(0,0,0,0.04); }}
    .box-luna {{ background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important; border: 1px solid #cbd5e1 !important; }}
    .box-sole {{ background: linear-gradient(135deg, #FFD600 0%, #FFB800 100%) !important; color: #1e293b !important; border: none !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .prezzo-rosa {{ color: #ec4899; font-size: 28px; font-weight: 900; margin-top: 10px; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 20px; background: #FFFFFF; border-radius: 25px; margin-bottom: 15px; border-left: 8px solid #f43f5e; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 25px; border-radius: 25px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA DI ACCESSO BLOCCANTE
# ==========================================
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("login_form"):
            e = st.text_input("Email").strip().lower()
            p = st.text_input("Password", type="password").strip()
            if st.form_submit_button("ENTRA"):
                db = carica_db()
                if not db.empty:
                    # Controllo incrociato email e password (con hashing)
                    match = db[(db['email'].str.lower() == e) & (db['password'] == hash_password(p))]
                    if not match.empty:
                        st.session_state.loggato = True
                        st.session_state.user_data = match.iloc[-1].to_dict()
                        st.rerun()
                    else: st.error("Email o Password errati")
                else: st.error("Database in caricamento... Riprova.")

    with t2:
        with st.form("reg_form"):
            re = st.text_input("La tua migliore Email")
            rp = st.text_input("Scegli Password", type="password")
            rn = st.text_input("Nome Genitore")
            rb = st.text_input("Nome Bambino")
            rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            rl = st.selectbox("Punto di ritiro preferito", ["Locker Milano", "Locker Roma", "Locker Torino", "InPost Locker"])
            if st.form_submit_button("CREA ACCOUNT"):
                if re and rp:
                    nuovo = {
                        "email": re.strip().lower(), "password": hash_password(rp),
                        "nome_genitore": rn, "nome_bambino": rb, "taglia": rt,
                        "data_inizio": str(date.today()), "scadenza": str(date.today() + timedelta(days=90)),
                        "locker": rl
                    }
                    registra_user(nuovo)
                    st.success("Registrato! Ora puoi fare il Login.")
                    st.balloons()
    st.stop()
