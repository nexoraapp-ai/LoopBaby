import streamlit as st
import pandas as pd
import requests
import base64
import os
import json
from datetime import date, datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE (TUA LOGICA SHEETDB) ---
SHEETDB_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def registra_utente(email, password):
    payload = {
        "data": [{
            "email": email,
            "password": password,
            "nome_genitore": "Mamma",
            "nome_bambino": "",
            "taglia": "50-56 cm",
            "data_inizio": str(date.today()),
            "scadenza": "",
            "locker": ""
        }]
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(SHEETDB_URL, json=payload, headers=headers)
    return r.text

def login(email, password):
    try:
        # Nota: SheetDB restituisce direttamente una lista di dizionari, non serve .get("data")
        r = requests.get(SHEETDB_URL)
        utenti = r.json()
        for u in utenti:
            if str(u.get("email")).strip().lower() == email.strip().lower() and str(u.get("password")) == str(password):
                st.session_state.user_data = u # Salviamo i dati per il profilo
                return True
    except Exception as e:
        st.error(f"Errore connessione: {e}")
    return False

# --- 2. CONFIGURAZIONE PAGINA & STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS PROFESSIONALE INTEGRALE ---
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
        margin-bottom: 35px; border-radius: 0 0 35px 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; height: 48px; border: none !important;
    }}
    .card {{ border-radius: 25px; padding: 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); margin-bottom: 15px; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SCHERMATA LOGIN (BLOCCANTE) ---
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div style="color:white; font-size:30px; font-weight:800;">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
    
    scelta = st.radio("Cosa vuoi fare?", ["Accedi", "Registrati"], horizontal=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if scelta == "Registrati":
        if st.button("CREA ACCOUNT"):
            if email and password:
                registra_utente(email, password)
                st.success("Registrazione completata! Ora fai login.")
            else: st.error("Inserisci email e password")

    if scelta == "Accedi":
        if st.button("ENTRA"):
            if login(email, password):
                st.session_state.loggato = True
                st.rerun()
            else: st.error("Credenziali errate")
    st.stop() # Blocca l'esecuzione qui finché non sei loggato

# --- 5. APP DOPO IL LOGIN (THE FULL EXPERIENCE) ---
# Barra Navigazione Fissa a 7 icone
c_nav = st.columns(7)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with c_nav[i]:
        label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
        if st.button(label, key=f"n_{pag}"): vai(pag)

st.divider()

if st.session_state.pagina == "Home":
    st.markdown('<div class="header-custom"><div style="color:white; font-size:30px; font-weight:800;">LOOPBABY</div></div>', unsafe_allow_html=True)
    img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_nome = st.session_state.user_data.get('nome_genitore', 'Mamma')
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
        <div><div style="font-size:28px; font-weight:800;">Ciao {u_nome}! 👋</div>
        <div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div></div>
        <div>{img_h}</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown("### Come funziona LoopBaby 🔄")
    st.markdown('<div class="card" style="text-align:left;"><b>1. Scegli Box:</b> Nel Locker scelto.<br><b>2. Controllo:</b> Hai 48 ore.<br><b>3. Utilizzo:</b> Massimo 3 mesi.</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f"### Profilo di {u.get('email')} 👤")
    st.write(f"**Taglia:** {u.get('taglia')}")
    if st.button("Logout"): 
        st.session_state.loggato = False
        st.rerun()

elif st.session_state.pagina == "Box":
    st.markdown("### Scegli la Box 📦")
    for s in ["LUNA 🌙", "SOLE ☀️"]:
        st.markdown(f'<div class="card"><h3>{s}</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
        if st.button(f"Scegli {s}"): st.session_state.carrello.append(s); st.toast("Aggiunto!")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown("### Chi siamo ❤️")
    st.markdown('<div class="card">Siamo genitori come te. LoopBaby nasce per dire basta allo spreco. 🌿</div>', unsafe_allow_html=True)
