import streamlit as st
import os
import base64
import json
import requests
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE (SHEETDB)
# ==========================================
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def registra_utente(email, password, nome, bimbo, taglia, locker):
    payload = {
        "data": [{
            "email": email.strip().lower(),
            "password": str(password).strip(),
            "nome_genitore": nome,
            "nome_bambino": bimbo,
            "taglia": taglia,
            "data_inizio": str(date.today()),
            "scadenza": str(date.today() + timedelta(days=90)),
            "locker": locker
        }]
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(SHEETDB_URL, json=payload, headers=headers)
    return r.status_code

def login(email, password):
    try:
        # Cache buster per leggere dati sempre freschi
        t = datetime.now().microsecond
        r = requests.get(f"{SHEETDB_URL}?t={t}")
        utenti = r.json()
        # SheetDB restituisce una lista di dizionari
        for u in utenti:
            if str(u.get("email")).strip().lower() == email.strip().lower() and str(u.get("password")).strip() == str(password).strip():
                return u 
    except: pass
    return None

# ==========================================
# 2. CONFIGURAZIONE E STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# ==========================================
# 3. CSS TOTALE (TUO DESIGN ORIGINALE)
# ==========================================
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important;
    }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; }}
    .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }} 
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. SCHERMATA ACCESSO (LOGIN/REG BLOCCANTE)
# ==========================================
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
    
    tab_l, tab_r = st.tabs(["Accedi", "Registrati"])
    
    with tab_l:
        with st.form("login_form"):
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                user = login(e, p)
                if user:
                    st.session_state.loggato = True
                    st.session_state.user_data = user
                    st.rerun()
                else: st.error("Email o Password errati")
    
    with tab_r:
        with st.form("reg_form"):
            re = st.text_input("Email")
            rp = st.text_input("Password", type="password")
            rn = st.text_input("Il tuo Nome")
            rb = st.text_input("Nome Bambino")
            rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste Italiane"])
            if st.form_submit_button("CREA ACCOUNT"):
                if re and rp:
                    if registra_utente(re, rp, rn, rb, rt, rl) == 201:
                        st.success("Registrato! Ora fai login.")
                else: st.error("Inserisci i dati richiesti")
    st.stop()

# ==========================================
# 5. APP DOPO LOGIN (THE FULL EXPERIENCE)
# ==========================================
st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# Barra Navigazione Fissa a 7 icone
c_nav = st.columns(7)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with c_nav[i]:
        label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and len(st.session_state.carrello)>0 else icon
        if st.button(label, key=f"nav_{pag}"): vai(pag)

st.divider()

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_nome = st.session_state.user_data.get('nome_genitore', 'Mamma')
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
        <div>
            <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_nome}! 👋</div>
            <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore.</div>
        </div>
        <div>{img_html}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            <b>1. Scegli e Ricevi:</b> Nel Locker scelto.<br><br>
            <b>2. Controllo Qualità:</b> Hai 48 ore.<br><br>
            <b>3. Utilizzo:</b> Massimo 3 mesi.<br><br>
            <b>🚚 Spedizioni:</b> Se continui il ciclo, paghiamo noi andata e ritorno!</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    tg = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f'<div style="text-align:center;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700;">📍 TAGLIA: {tg}</span></div>', unsafe_allow_html=True)
    for s, c in [("LUNA 🌙", "box-luna"), ("SOLE ☀️", "box-sole")]:
        st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        if st.button(f"Scegli {s}", key=s): st.session_state.carrello.append(s); st.toast("Aggiunto!")

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
        <b>👤 Nome:</b> {u.get('nome_genitore')}<br><b>📧 Email:</b> {u.get('email')}<br>
        <b>📏 Taglia:</b> {u.get('taglia')}<br><b>📍 Locker:</b> {u.get('locker')}
    </div>""", unsafe_allow_html=True)
    if st.button("Logout"): 
        st.session_state.loggato = False
        st.rerun()

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2><b>Siamo genitori come te.</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="obiettivo-pink"><b>Il nostro obiettivo?</b><br>Risparmio e futuro migliore per i nostri figli.</div>', unsafe_allow_html=True)
