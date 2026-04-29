import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (IL TUO LINK SHEETDB) ---
API_URL = "https://sheetdb.io/api/v1/i2g703uwrn9sr"

def carica_db():
    try:
        res = requests.get(API_URL)
        return pd.DataFrame(res.json()) if res.status_code == 200 else pd.DataFrame()
    except: return pd.DataFrame()

def aggiungi_utente(nuovo_utente):
    requests.post(API_URL, json={"data": [nuovo_utente]})

def aggiorna_utente(email, dati_nuovi):
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati_nuovi})

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

img, logo = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. CSS PROFESSIONALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 30px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; border: none !important; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 20px; border: 1px solid #f87171; font-weight: 800; margin: 15px; text-align: center; font-size: 14px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df = carica_db()

if st.session_state.user is None:
    st.markdown(f'<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding: 0 20px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e = st.text_input("Email", key="l_e")
                p = st.text_input("Password", type="password", key="l_p")
                if st.form_submit_button("ENTRA"):
                    user = df[(df['email'] == e) & (df['password'].astype(str) == str(p))]
                    if not user.empty:
                        st.session_state.user = user.iloc[0].to_dict()
                        vai("Home")
                    else: st.error("Email o Password errati")
        with t2:
            with st.form("r"):
                er = st.text_input("La tua migliore Email", key="r_e")
                pr = st.text_input("Scegli Password", key="r_p")
                if st.form_submit_button("CREA ACCOUNT"):
                    if not df.empty and er in df['email'].values: st.error("Esiste già!")
                    else:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        nuovo = {"email": er, "password": str(pr), "nome_genitore": "Mamma", "nome_bambino": "---", "taglia": "---", "data_inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad}
                        aggiungi_utente(nuovo)
                        st.success("Account creato! Ora fai l'accesso.")
else:
    # --- LOGICA AVVISI SCADENZA ---
    scad_str = str(st.session_state.user.get('scadenza', ''))
    if scad_str != 'nan' and scad_str != '':
        giorni = (datetime.strptime(scad_str, "%Y-%m-%d") - datetime.now()).days
        if 0 <= giorni <= 10:
            st.markdown(f'<div class="avviso-scadenza">⚠️ ATTENZIONE: Mancano {giorni} giorni al termine della tua Box! Prepariamo la nuova taglia?</div>', unsafe_allow_html=True)

    if st.session_state.pagina == "Home":
        st.markdown(f'<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user['nome_genitore']
        st.markdown(f"### Ciao {nome}! 👋")
        if img: st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:25px;">', unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Logout"): 
            st.session_state.user = None
            vai("Welcome")

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Il tuo Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.user['nome_genitore'])
            nb = st.text_input("Nome Bimbo", st.session_state.user['nome_bambino'])
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA SUL FOGLIO GOOGLE"):
                aggiorna_utente(st.session_state.user['email'], {"nome_genitore": n, "nome_bambino": nb, "taglia": tg})
                st.session_state.user.update({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})
                st.success("Dati aggiornati su Excel!")

    elif st.session_state.pagina == "Info":
        st.markdown("## Come Funziona 🔄")
        st.markdown('<div class="card" style="text-align:left; font-size:14px;">1. <b>Scegli</b> la box.<br>2. <b>Ricevi</b> e controlla qualità in 48h.<br>3. <b>Usa</b> per massimo 3 mesi.<br>4. <b>Decidi:</b> rendi o prendi la nuova taglia.<br>5. <b>Patto del 10:</b> rendi 10 capi per riceverne 10.</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("## Chi Siamo ❤️")
        st.markdown('<div class="card">Siamo genitori come te. LoopBaby nasce per ridurre gli sprechi e far risparmiare le famiglie offrendo capi di qualità.</div>', unsafe_allow_html=True)

    # --- NAV BAR FISSA ---
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📖", "Info"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
