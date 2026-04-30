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
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except: return pd.DataFrame()

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
    return requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"}).status_code

def login_check(email, password):
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
# 3. CSS DESIGN (LOOK 23:30)
# ==========================================
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
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

# ==========================================
# 4. LOGICA ACCESSO
# ==========================================
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("l"):
            e, p = st.text_input("Email").strip().lower(), st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                u = login_check(e, p)
                if u: st.session_state.loggato, st.session_state.user_data = True, u; st.rerun()
                else: st.error("Dati errati")
    with t2:
        with st.form("r"):
            re, rp = st.text_input("Email"), st.text_input("Scegli Password")
            rn, rb = st.text_input("Nome Genitore"), st.text_input("Nome Bambino")
            rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste"])
            if st.form_submit_button("CREA ACCOUNT"):
                if registra_utente(re, rp, rn, rb, rt, rl) == 201: st.success("Registrato! Ora accedi."); st.balloons()
    st.stop()

# ==========================================
# 5. APP DOPO LOGIN
# ==========================================
cols = st.columns(7)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with cols[i]:
        lbl = f"{icon}({len(st.session_state.carrello)})" if pag=="Carrello" and st.session_state.carrello else icon
        if st.button(lbl, key=f"n_{pag}"): vai(pag)
st.divider()

if st.session_state.pagina == "Home":
    img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_n = st.session_state.user_data.get('nome_genitore', 'Mamma')
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
        <div><div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_n}! 👋</div>
        <div style="font-size:14px; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino.</div></div>
        <div>{img_h}</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Mamme Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
    if st.button("Partecipa"): vai("PromoDettaglio")

elif st.session_state.pagina == "PromoDettaglio":
    st.markdown("### Diventa Fondatrice 🌸")
    with st.form("p_f"):
        p, d = st.text_input("Peso (kg)"), st.text_input("Dimensioni pacco")
        if st.form_submit_button("RICHIEDI ETICHETTA"): st.success("Richiesta inviata!")

elif st.session_state.pagina == "Info":
    st.markdown("### Come funziona LoopBaby 🔄")
    st.write("1. Ricevi la Box nel Locker. 2. Usala per 3 mesi. 3. Scambia o Rendi.")
    st.markdown("### Il Patto del 10 📍")
    st.markdown('<div class="card">Rendi 10 capi per riceverne 10 nuovi.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    tg = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f"**TAGLIA ATTIVA: {tg}**")
    q = st.radio("Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c in [("LUNA 🌙", "box-luna"), ("SOLE ☀️", "box-sole")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(s, 19.90)
    else:
        st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><div style="font-size:24px;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button("Scegli Premium"): aggiungi_al_carrello("Premium", 29.90)

elif st.session_state.pagina == "ChiSiamo":
    st.markdown("### Chi Siamo ❤️")
    st.markdown('<div class="card">Siamo genitori stanchi dello spreco. Abbiamo creato LoopBaby per far viaggiare la qualità di famiglia in famiglia. 🌿</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f"### Profilo 👤")
    st.write(f"**Nome:** {u.get('nome_genitore')} | **Taglia:** {u.get('taglia')}")
    if st.button("Logout"): st.session_state.loggato = False; st.rerun()

elif st.session_state.pagina == "Carrello":
    st.markdown("### Carrello 🛒")
    if not st.session_state.carrello: st.write("Vuoto.")
    else:
        tot = sum(i['prezzo'] for i in st.session_state.carrello)
        for i in st.session_state.carrello: st.write(f"✅ {i['nome']} - {i['prezzo']}€")
        st.markdown(f"### Totale: {tot:.2f}€")
