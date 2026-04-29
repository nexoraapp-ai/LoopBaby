import streamlit as st
import pandas as pd
import urllib3
import json
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (USA IL NUOVO LINK) ---
API_URL = "INCOLLA_QUI_IL_NUOVO_LINK_DI_SHEETDB"

def carica_db():
    http = urllib3.PoolManager()
    try:
        t = datetime.now().timestamp()
        r = http.request('GET', f"{API_URL}?t={t}")
        if r.status == 200:
            df = pd.DataFrame(json.loads(r.data.decode('utf-8')))
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza'])
    except:
        return pd.DataFrame()

def aggiungi_utente(email, password):
    http = urllib3.PoolManager()
    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    
    # Prepariamo il pacchetto dati identico al test ReqBin
    nuovo_dato = {
        "email": str(email).strip(),
        "password": str(password).strip(),
        "nome": "Mamma",
        "bimbo": "---",
        "taglia": "---",
        "inizio": datetime.now().strftime("%Y-%m-%d"),
        "scadenza": scad
    }
    
    encoded_data = json.dumps({"data": [nuovo_dato]}).encode('utf-8')
    
    try:
        # Usiamo urllib3 per simulare ReqBin senza filtri
        r = http.request(
            'POST', 
            API_URL,
            body=encoded_data,
            headers={'Content-Type': 'application/json'}
        )
        return r.status
    except:
        return 500

# --- 2. SETUP APP ---
st.set_page_config(page_title="LoopBaby", layout="centered")
if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 30px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; height: 50px; border: none !important; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df_globale = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty:
                        m = df_globale[(df_globale['email'].astype(str).str.lower() == e.lower()) & (df_globale['password'].astype(str) == str(p))]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati")
        with t2:
            with st.form("r"):
                er = st.text_input("Email ")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    with st.spinner("Salvataggio in corso..."):
                        status = aggiungi_utente(er, pr)
                    if status == 201:
                        st.success("✅ REGISTRATO! Ora puoi accedere.")
                        st.balloons()
                    else:
                        st.error(f"Errore {status}. SheetDB ha rifiutato i dati.")
else:
    # --- HOME ---
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    nome = st.session_state.user.get('nome', 'Mamma')
    st.markdown(f"### Ciao {nome}! 👋")
    if img_data: st.markdown(f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">', unsafe_allow_html=True)
    if st.button("Logout"): 
        st.session_state.user = None
        vai("Welcome")
