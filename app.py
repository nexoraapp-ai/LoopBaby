import streamlit as st
import pandas as pd
import requests
import base64
import os
from datetime import date, datetime, timedelta

# --- 1. CONNESSIONE DIRETTA ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Carichiamo i dati fregandocene della cache
        res = requests.get(f"{API_URL}?t={datetime.now().microsecond}")
        return pd.DataFrame(res.json())
    except: return pd.DataFrame()

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")
if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# --- 3. CSS E IMMAGINI (LOOK ORIGINALE) ---
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7; max-width: 450px; margin: 0 auto; }}
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; border-radius: 0 0 30px 30px; margin-bottom: 30px; display: flex; align-items: center; justify-content: center; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 20px; width: 100%; font-weight: 800; border: none; height: 45px; }}
    .card {{ border-radius: 25px; padding: 20px; border: 1px solid #EAE2D6; background: white; box-shadow: 0 8px 25px rgba(0,0,0,0.03); margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO ---
df = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    
    with tab1:
        with st.form("login_form"):
            email_input = st.text_input("Email").strip().lower()
            pass_input = st.text_input("Password", type="password").strip()
            if st.form_submit_button("ENTRA"):
                if not df.empty:
                    # CONFRONTO DIRETTO: Nessun hash, nessuna complicazione
                    df['email_low'] = df['email'].astype(str).str.lower().str.strip()
                    df['pass_str'] = df['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                    
                    match = df[(df['email_low'] == email_input) & (df['pass_str'] == pass_input)]
                    
                    if not match.empty:
                        st.session_state.user = match.iloc[-1].to_dict()
                        vai("Home")
                    else:
                        st.error("Credenziali non trovate. Controlla l'Excel!")
                else:
                    st.error("Il database è vuoto. Registrati!")

    with tab2:
        with st.form("reg_form"):
            re = st.text_input("Email")
            rp = st.text_input("Password")
            rn = st.text_input("Nome")
            if st.form_submit_button("CREA ACCOUNT"):
                requests.post(API_URL, json={"data": [{"email": re, "password": rp, "nome_genitore": rn}]})
                st.success("Registrato! Ora fai l'accesso.")

else:
    # --- APP DOPO LOGIN ---
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    nome = st.session_state.user.get('nome_genitore', 'Mamma')
    st.title(f"Ciao {nome}! 👋")
    if img_data: st.markdown(f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">', unsafe_allow_html=True)
    
    # BARRA NAVIGAZIONE
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📖", "Info"), ("👤", "Profilo"), ("🛒", "Carrello")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
