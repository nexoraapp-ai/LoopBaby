import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE (ULTRA-ROBUSTA)
# ==========================================
API_URL = "https://sheetdb.io"
SHEET_ID = "14mSfOS3lPs5_EdCEKwBGvhDIKnU-H5quZUk5e31X5s8"
# Link di emergenza alternativo
CSV_URL = f"https://google.com{SHEET_ID}/export?format=csv&gid=0"

def carica_db():
    # Metodo A: SheetDB (Il più veloce)
    try:
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=3)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
    except: pass

    # Metodo B: Scaricamento CSV diretto (Il più sicuro)
    try:
        df_direct = pd.read_csv(CSV_URL)
        if not df_direct.empty:
            df_direct.columns = [str(c).strip().lower() for c in df_direct.columns]
            return df_direct
    except: pass
    
    # Metodo C: Struttura vuota se Google è offline
    return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])

def registra_user(dati):
    requests.post(API_URL, json={"data": [dati]})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ==========================================
# 2. CONFIGURAZIONE PAGINA & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# ==========================================
# 3. DESIGN CSS INTEGRALE (LOOK 23:30)
# ==========================================
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

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
        margin-bottom: 35px; border-radius: 0 0 40px 40px; box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 4px; text-transform: uppercase; text-shadow: 2px 2px 15px rgba(0,0,0,0.5); }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 25px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 52px; font-size: 16px; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
    }}
    
    .card {{ border-radius: 30px; padding: 25px; margin: 10px 10px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 12px 35px rgba(0,0,0,0.04); }}
    .box-luna {{ background: #f1f5f9 !important; border: 1px solid #cbd5e1 !important; }}
    .box-sole {{ background: #FFD600 !important; color: #1e293b !important; border: none !important; }}
    .prezzo-rosa {{ color: #f43f5e; font-size: 28px; font-weight: 900; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 20px; background: #FFFFFF; border-radius: 25px; margin-bottom: 15px; border-left: 8px solid #f43f5e; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA ACCESSO
# ==========================================
df_db = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Vestili bene, falli crescere bene. 🔄</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")

    elif st.session_state.pagina == "Login":
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        with tab1:
            with st.form("l"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_db.empty:
                        hp = hash_password(p)
                        df_db['p_fix'] = df_db['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        match = df_db[(df_db['email'].astype(str).str.lower() == e) & (df_db['p_fix'] == hp)]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
                    else: st.error("Connessione in corso... Riprova tra 5 secondi.")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Password", type="password")
                rn = st.text_input("Nome Genitore")
                rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
                rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste"])
                if st.form_submit_button("CREA ACCOUNT"):
                    nuovo = {"email": re.strip().lower(), "password": hash_password(rp), "nome_genitore": rn, "taglia": rt, "data_inizio": str(date.today()), "locker": rl}
                    registra_user(nuovo)
                    st.success("Registrato! Ora fai l'Accedi.")
                    st.balloons()

# ==========================================
# 5. APP DOPO LOGIN
# ==========================================
else:
    # NAVIGAZIONE FISSA
    c_nav = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"n_{pag}"): vai(pag)
    st.divider()

    if st.session_state.pagina == "Home":
        nome = st.session_state.user.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:35px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; padding: 0 10px;">
            <div><div style="font-size:34px; font-weight:800;">Ciao {nome}! 👋</div>
            <div style="font-size:16px; color:#475569;">Il tuo armadio circolare è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #f43f5e;">✨ <b>Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("### La nostra Storia ❤️")
        st.markdown('<div class="card" style="text-align:left; line-height:1.7;">Ma quanto è brutto quando quella tutina che ami già non entra più? LoopBaby nasce per dire basta allo spreco. 🌿</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "Box":
        for s, c, p in [("LUNA 🌙", "box-luna", 19.90), ("SOLE ☀️", "box-sole", 19.90)]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): st.session_state.carrello.append({"n": s, "p": p}); st.toast("Aggiunto!")
