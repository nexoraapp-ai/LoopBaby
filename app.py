import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. DATABASE & SICUREZZA (FIX DEFINITIVO)
# ==========================================
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Forza SheetDB a darci i dati reali
        res = requests.get(f"{API_URL}?t={datetime.now().microsecond}")
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except: return pd.DataFrame()

def registra_user(dati):
    # Forza l'invio corretto dei dati su Excel
    headers = {"Content-Type": "application/json"}
    payload = {"data": [dati]}
    r = requests.post(API_URL, json=payload, headers=headers)
    return r.status_code

def hash_psw(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ==========================================
# 2. CONFIGURAZIONE & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_b64("bimbo.jpg"), get_b64("logo.png")

# ==========================================
# 3. CSS TOTALE (LOOK 23:30)
# ==========================================
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 100px !important; }}
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; border: none !important; height: 48px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA ACCESSO (LOGIN / REGISTER)
# ==========================================
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t1:
        with st.form("login"):
            e = st.text_input("Email").strip().lower()
            p = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                db = carica_db()
                if not db.empty:
                    # Fix Excel password numbers (.0)
                    db['p_fix'] = db['password'].astype(str).str.replace('.0','',regex=False).str.strip()
                    user = db[(db['email'].str.lower() == e) & (db['p_fix'] == hash_psw(p))]
                    if not user.empty:
                        st.session_state.loggato = True
                        st.session_state.user_data = user.iloc[-1].to_dict()
                        st.rerun()
                    else: st.error("Email o Password errati")
                else: st.error("Errore database. Riprova.")

    with t2:
        with st.form("reg"):
            re = st.text_input("Email")
            rp = st.text_input("Scegli Password", type="password")
            rn = st.text_input("Nome Genitore")
            rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("CREA ACCOUNT"):
                if re and rp:
                    nuovo = {"email": re.strip().lower(), "password": hash_psw(rp), "nome_genitore": rn, "taglia": rt, "data_inizio": str(date.today())}
                    if registra_user(nuovo) == 201:
                        st.success("Registrato! Ora puoi accedere.")
                        st.balloons()
                    else: st.error("Errore salvataggio. Controlla SheetDB!")
    st.stop()

# ==========================================
# 5. APP DOPO LOGIN (TUTTE LE PAGINE)
# ==========================================
# Barra Navigazione Fissa (7 ICONE)
c_nav = st.columns(7)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with c_nav[i]:
        label = f"{icon}({len(st.session_state.carrello)})" if pag=="Carrello" and st.session_state.carrello else icon
        if st.button(label, key=f"n_{pag}"): vai(pag)
st.divider()

if st.session_state.pagina == "Home":
    img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_n = st.session_state.user_data.get('nome_genitore', 'Mamma')
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
        <div><div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_n}! 👋</div>
        <div style="font-size:14px; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino.</div></div>
        <div>{img_h}</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b>✨ Promo Mamme Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown("### Come funziona LoopBaby 🔄")
    st.markdown("""<div class="card" style="text-align:left; font-size:14px;">1. Scegli Box.<br>2. Usala per 3 mesi.<br>3. Scambia con la taglia nuova.<br><b>Spedizioni Gratis</b> se continui!</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    tg = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f"<div style='text-align:center;'><b>TAGLIA ATTIVA: {tg}</b></div>", unsafe_allow_html=True)
    for s, c in [("LUNA 🌙", "box-luna"), ("SOLE ☀️", "box-sole")]:
        st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        if st.button(f"Scegli {s}", key=s): st.session_state.carrello.append(s); st.toast("Aggiunto!")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown("### La nostra Storia ❤️")
    st.markdown('<div class="card" style="text-align:left;">Ma quanto è brutto quando quella tutina che ami già non entra più? 💸 LoopBaby nasce per dire basta allo spreco.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f"""<div class="card" style="text-align:left;"><b>👤 Nome:</b> {u.get('nome_genitore')}<br><b>📏 Taglia:</b> {u.get('taglia')}</div>""", unsafe_allow_html=True)
    if st.button("LOGOUT"): st.session_state.loggato = False; st.rerun()
