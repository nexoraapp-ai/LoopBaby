import streamlit as st
import os
import base64
import json
import requests
from datetime import date, datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE (LOGICA SHEETDB ESTRATTA) ---
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def registra_utente(email, password, nome, bimbo, taglia, locker):
    payload = {
        "data": [{
            "email": email.strip().lower(),
            "password": password,
            "nome_genitore": nome,
            "nome_bambino": bimbo,
            "taglia": taglia,
            "data_inizio": str(date.today()),
            "scadenza": "",
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
        for u in utenti:
            if str(u.get("email")).strip().lower() == email.strip().lower() and str(u.get("password")) == str(password):
                return u # Restituisce l'intera riga dell'utente
    except: pass
    return None

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(nome_pag): 
    st.session_state.pagina = nome_pag
    st.rerun()

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 3. CSS TOTALE (DESIGN ORIGINALE INTEGRALE) ---
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
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; height: 45px;
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN / REGISTRAZIONE (BLOCCANTE) ---
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
    
    scelta = st.radio("Accesso", ["Login", "Registrati"], horizontal=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if scelta == "Registrati":
        nome = st.text_input("Il tuo Nome")
        bimbo = st.text_input("Nome del piccolo")
        taglia = st.selectbox("Taglia attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
        locker = st.selectbox("Locker preferito", ["InPost", "Esselunga", "Poste Italiane"])
        if st.button("CREA ACCOUNT"):
            if email and password:
                if registra_utente(email, password, nome, bimbo, taglia, locker) == 201:
                    st.success("Registrazione completata! Ora fai login.")
            else: st.error("Inserisci email e password")

    if scelta == "Login":
        if st.button("ENTRA"):
            user = login(email, password)
            if user:
                st.session_state.loggato = True
                st.session_state.user_data = user
                st.rerun()
            else: st.error("Credenziali errate")
    st.stop()

# --- 5. APP DOPO IL LOGIN (THE FULL EXPERIENCE) ---
st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

if st.session_state.pagina == "Home":
    img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_nome = st.session_state.user_data.get('nome_genitore', 'Mamma').split()[0]
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
        <div>
            <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_nome}! 👋</div>
            <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div>
            <div style="margin-top:15px;">
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px;">👶 Capi di qualità selezionati</div>
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px;">🔄 Cambi quando cresce</div>
            </div>
        </div>
        <div>{img_html}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>!</p></div>""", unsafe_allow_html=True)
    if st.button("Partecipa ora"): vai("PromoDettaglio")

elif st.session_state.pagina == "PromoDettaglio":
    st.markdown('<h2 style="text-align:center;">Diventa Fondatrice 🌸</h2>', unsafe_allow_html=True)
    with st.form("promo_f"):
        p, d = st.text_input("Peso stimato (kg)"), st.text_input("Dimensioni pacco")
        if st.form_submit_button("RICHIEDI ETICHETTA"): st.success("Richiesta inviata!")
    if st.button("Torna in Home"): vai("Home")

elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            <b>1. Scegli e Ricevi:</b> Nel Locker scelto.<br><br>
            <b>2. Controllo Qualità:</b> Hai 48 ore.<br><br>
            <b>3. Utilizzo:</b> Massimo 3 mesi.<br><br>
            <b>🚚 Spedizioni:</b> Se continui, paghiamo noi andata e ritorno!</div>""", unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;">Il Patto del 10 📍</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px;">♻️ <b>Equilibrio:</b> Rendi 10 capi per riceverne 10 nuovi.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    tg = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f'<div style="text-align:center;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700;">📍 CONFIGURATA PER: {tg}</span></div>', unsafe_allow_html=True)
    for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace")]:
        st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(s, 19.90)

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown('<h2 style="text-align:center;">Profilo 👤</h2>', unsafe_allow_html=True)
    st.markdown(f"""<div class="card" style="text-align:left; font-size:14px;">
        <b>👤 Nome:</b> {u.get('nome_genitore')}<br><b>📧 Email:</b> {u.get('email')}<br>
        <b>👶 Bimbo:</b> {u.get('nome_bambino')}<br><b>📏 Taglia:</b> {u.get('taglia')}<br>
        <b>📍 Locker:</b> {u.get('locker')}
    </div>""", unsafe_allow_html=True)
    if st.button("Logout"): st.session_state.loggato = False; st.rerun()

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<h2 style="text-align:center;">Chi siamo? ❤️</h2>', unsafe_allow_html=True)
    st.markdown('<div class="obiettivo-pink"><b>Obiettivo:</b> Risparmiare e proteggere il pianeta.</div>', unsafe_allow_html=True)

# --- NAV BAR FISSA (7 COLONNE) ---
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
c = st.columns(7)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with c[i]:
        label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and len(st.session_state.carrello)>0 else icon
        if st.button(label, key=f"nav_{pag}"): vai(pag)
