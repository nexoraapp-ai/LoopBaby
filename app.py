import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        timestamp = datetime.now().timestamp()
        res = requests.get(f"{API_URL}?t={timestamp}")
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                # PULIZIA TOTALE: toglie spazi all'inizio e alla fine dei nomi colonne
                df.columns = [str(c).strip() for c in df.columns]
                return df
        return pd.DataFrame()
    except: return pd.DataFrame()

def aggiungi_utente(nuovo):
    requests.post(API_URL, json={"data": [nuovo]})

def aggiorna_utente(email, dati):
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati})

# --- 2. CONFIGURAZIONE PAGINA ---
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
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; background-position: center; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 20px; border: 1px solid #f87171; font-weight: 800; margin: 15px; text-align: center; font-size: 13px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l_f"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df.empty and 'email' in df.columns:
                        match = df[(df['email'].str.lower() == e.lower()) & (df['password'].astype(str) == str(p))]
                        if not match.empty:
                            st.session_state.user = match.iloc[0].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
                    else: st.error("Database in aggiornamento...")
        with t2:
            with st.form("r_f"):
                er = st.text_input("Email ")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if not df.empty and er.lower() in df['email'].str.lower().values:
                        st.error("Esiste già!")
                    else:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        # Usiamo i nomi puliti che SheetDB invierà all'Excel
                        nuovo = {"email": er, "password": str(pr), "nome genitore": "Mamma", "nome bambino": "---", "taglia": "---", "data inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad}
                        aggiungi_utente(nuovo)
                        st.success("Creato! Ora fai l'accesso.")
else:
    # --- LOGICA AVVISI ---
    scad_str = str(st.session_state.user.get('scadenza', ''))
    if scad_str != 'nan' and scad_str != '':
        try:
            giorni = (datetime.strptime(scad_str, "%Y-%m-%d") - datetime.now()).days
            if 0 <= giorni <= 10:
                st.markdown(f'<div class="avviso-scadenza">⚠️ ATTENZIONE: Mancano {giorni} giorni al cambio Box!</div>', unsafe_allow_html=True)
        except: pass

    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome genitore', 'Mamma')
        st.markdown(f"### Ciao {nome}! 👋")
        if img_data: st.markdown(f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">', unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; vai("Welcome")

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        with st.form("p_f"):
            n = st.text_input("Tuo Nome", st.session_state.user.get('nome genitore', ''))
            nb = st.text_input("Nome Bambino", st.session_state.user.get('nome bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA SU EXCEL"):
                # Qui aggiorniamo SheetDB usando i nomi delle colonne dell'Excel
                aggiorna_utente(st.session_state.user['email'], {"nome genitore": n, "nome bambino": nb, "taglia": tg})
                st.session_state.user.update({"nome genitore": n, "nome bambino": nb, "taglia": tg})
                st.success("Dati aggiornati correttamente!")

    # Nav
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📖", "Info"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag)
