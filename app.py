import streamlit as st
import pandas as pd
import requests
import base64
import os
from datetime import date, datetime, timedelta

# --- DATABASE ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        res = requests.get(f"{API_URL}?t={datetime.now().timestamp()}")
        return pd.DataFrame(res.json()) if res.status_code == 200 else pd.DataFrame()
    except: return pd.DataFrame()

def registra_utente(email, password, nome, bimbo, taglia, locker):
    payload = {"data": [{"email": email.strip().lower(), "password": password, "nome_genitore": nome, "nome_bambino": bimbo, "taglia": taglia, "data_inizio": str(date.today()), "scadenza": str(date.today()+timedelta(days=90)), "locker": locker}]}
    return requests.post(API_URL, json=payload, headers={"Content-Type": "application/json"}).status_code

def login_check(email, password):
    try:
        r = requests.get(API_URL)
        for u in r.json():
            if str(u.get("email")).lower() == email.strip().lower() and str(u.get("password")) == str(password): return u
    except: pass
    return None

# --- CONFIG ---
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")
if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_b64(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_b64("bimbo.jpg"), get_b64("logo.png")

# --- CSS LOOK 23:30 ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; background-position: center; height: 130px; display: flex; align-items: center; justify-content: center; margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; height: 48px; border: none !important; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN LOGIC ---
if not st.session_state.loggato:
    st.markdown(f'<div class="header-custom"><div style="color:white; font-size:32px; font-weight:800;">LOOPBABY</div></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("l"):
            e, p = st.text_input("Email"), st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                u = login_check(e, p)
                if u: st.session_state.loggato, st.session_state.user_data = True, u; st.rerun()
                else: st.error("Dati errati")
    with t2:
        with st.form("r"):
            re, rp = st.text_input("Email"), st.text_input("Scegli Password")
            rn, rb = st.text_input("Tuo Nome"), st.text_input("Nome Bambino")
            rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste"])
            if st.form_submit_button("CREA ACCOUNT"):
                if registra_utente(re, rp, rn, rb, rt, rl) == 201: st.success("Registrato! Ora fai login.")
    st.stop()

# --- APP PAGES ---
st.markdown(f'<div class="header-custom"><div style="color:white; font-size:32px; font-weight:800;">LOOPBABY</div></div>', unsafe_allow_html=True)

if st.session_state.pagina == "Home":
    img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_n = st.session_state.user_data.get('nome_genitore', 'Mamma')
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
        <div><div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_n}! 👋</div>
        <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div>
        <div style="margin-top:15px; font-size:11px; color:#475569;">👶 Qualità selezionata | 🔄 Cambi quando cresce | 💰 Risparmi oltre 1000€</div></div>
        <div>{img_h}</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br>Dona 10 capi e ricevi una <b>BOX OMAGGIO</b>!</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown("<h2 style='text-align:center;'>Come funziona 🔄</h2>", unsafe_allow_html=True)
    st.markdown('<div style="padding:0 25px; font-size:14px; color:#475569; line-height:1.6;">1. Ricevi la Box nel Locker.<br>2. Hai 48h per il controllo qualità.<br>3. Tienila fino a 3 mesi.<br>4. Spedizioni gratis se continui il ciclo!</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Il Patto del 10 📍</h2>", unsafe_allow_html=True)
    st.markdown('<div class="card" style="text-align:left; font-size:13px;">♻️ Equilibrio: Rendi 10 capi per riceverne 10 nuovi della taglia successiva.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    tg = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f"<div style='text-align:center; margin-bottom:10px;'><span style='background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700;'>📍 TAGLIA: {tg}</span></div>", unsafe_allow_html=True)
    q = st.radio("Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): st.session_state.carrello.append(s); st.toast("Aggiunto!")
    else:
        st.markdown('<div class="card box-premium"><h3>PREMIUM 💎</h3><p>Capi nuovi o seminuovi</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button("Scegli Premium"): st.session_state.carrello.append("Premium"); st.toast("Aggiunto!")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<h2 style="text-align:center;">La nostra storia ❤️</h2>', unsafe_allow_html=True)
    st.markdown('<div style="padding:0 20px; font-size:14px; text-align:center; line-height:1.6;">Ma quanto è brutto quando quella tutina che ami non entra più? 💸 LoopBaby nasce per dire basta allo spreco.</div>', unsafe_allow_html=True)
    st.markdown('<div class="obiettivo-pink"><b>Obiettivo:</b> Lasciare un mondo migliore ai nostri figli.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f'<div class="card" style="text-align:left;"><b>👤 Nome:</b> {u.get("nome_genitore")}<br><b>📧 Email:</b> {u.get("email")}<br><b>📏 Taglia:</b> {u.get("taglia")}<br><b>📍 Locker:</b> {u.get("locker")}</div>', unsafe_allow_html=True)
    if st.button("LOGOUT"): st.session_state.loggato = False; st.rerun()

# --- NAVBAR 7 ICONE ---
st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
cols = st.columns(7)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with cols[i]:
        if st.button(icon, key=f"n_{pag}"): vai(pag)
