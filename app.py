import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONNESSIONE DATABASE ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Forziamo il caricamento dati freschi saltando la cache
        r = requests.get(f"{API_URL}?t={datetime.now().timestamp()}", timeout=10)
        if r.status_code == 200:
            df = pd.DataFrame(r.json())
            if not df.empty:
                # PULIZIA COLONNE: toglie spazi e rende minuscolo
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])
    except:
        return pd.DataFrame()

def aggiungi_utente(nuovo):
    return requests.post(API_URL, json={"data": [nuovo]}, timeout=15).status_code

def aggiorna_utente(email, dati):
    return requests.patch(f"{API_URL}/email/{email}", json={"data": dati}).status_code

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS PROFESSIONALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; border-radius: 0 0 30px 30px; display: flex; align-items: center; justify-content: center; margin-bottom: 35px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; border: none !important; height: 45px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO ---
df_globale = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("login_form"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty:
                        # CONFRONTO "MORBIDO": convertiamo tutto in stringa e togliamo i decimali (.0)
                        df_globale['email_str'] = df_globale['email'].astype(str).str.strip().str.lower()
                        df_globale['pass_str'] = df_globale['password'].astype(str).str.split('.').str[0].str.strip()
                        
                        user_match = df_globale[(df_globale['email_str'] == e) & (df_globale['pass_str'] == p)]
                        
                        if not user_match.empty:
                            st.session_state.user = user_match.iloc[-1].to_dict()
                            vai("Home")
                        else:
                            st.error("Email o Password errati. Riprova.")
                    else:
                        st.error("Il database è vuoto. Registrati prima!")
        with t2:
            with st.form("reg_form"):
                er = st.text_input("Email ")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if er and pr:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        nuovo = {"email": er.strip(), "password": pr.strip(), "nome": "Mamma", "bimbo": "---", "taglia": "---", "inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad, "locker": "Non impostato"}
                        if aggiungi_utente(nuovo) == 201:
                            st.success("✅ REGISTRATO! Ora puoi fare il login dalla scheda 'Accedi'.")
                            st.balloons()
                        else: st.error("Errore di connessione. Riprova.")

else:
    # --- APP DOPO LOGIN (HOME) ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome_u = st.session_state.user.get('nome', 'Mamma')
        st.markdown(f"### Ciao {nome_u}! 👋")
        if img_data: st.markdown(f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">', unsafe_allow_html=True)
        if st.button("Logout"): 
            st.session_state.user = None
            vai("Welcome")

    # BARRA NAVIGAZIONE FISSA (7 ICONE)
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(7)
    m_list = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(m_list):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
