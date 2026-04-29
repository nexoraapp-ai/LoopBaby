import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONNESSIONE GOOGLE SHEETS ---
# Usa questo link "pulito" per evitare errori di permessi
URL_FOGLIO = "https://google.com"

conn = st.connection("gsheets", type=GSheetsConnection)

def carica_dati():
    # Carica tutto il foglio. Se vuoto, restituisce un DataFrame con le colonne corrette.
    try:
        return conn.read(spreadsheet=URL_FOGLIO, ttl="1m")
    except:
        return pd.DataFrame(columns=['email', 'password', 'nome genitore', 'nome bambino', 'taglia', 'data inizio', 'scadenza'])

def salva_dati(df_nuovo):
    conn.update(spreadsheet=URL_FOGLIO, data=df_nuovo)
    st.cache_data.clear()

# --- 2. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "dati_utente" not in st.session_state: st.session_state.dati_utente = {}

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_base64(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img, logo = get_base64("bimbo.jpg"), get_base64("logo.png")

# --- 3. STILE CSS ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7; max-width: 450px; margin: 0 auto; padding-bottom: 100px; }}
    .header {{ background-image: linear-gradient(rgba(0,0,0,0.1),rgba(0,0,0,0.1)), url("data:image/png;base64,{logo}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 20px; }}
    .header-t {{ color: white; font-size: 30px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background: #f43f5e !important; color: white !important; border-radius: 15px; width: 100%; font-weight: 700; border: none; }}
    .card {{ border-radius: 20px; padding: 20px; margin: 10px; border: 1px solid #EAE2D6; background: white; }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 15px; border: 1px solid #f87171; font-weight: 800; text-align: center; margin: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df = carica_dati()

if st.session_state.user is None:
    st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            e = st.text_input("Email", key="l_e")
            p = st.text_input("Password", type="password", key="l_p")
            if st.button("ENTRA"):
                user_row = df[(df['email'] == e) & (df['password'].astype(str) == str(p))]
                if not user_row.empty:
                    st.session_state.user = e
                    st.session_state.dati_utente = user_row.iloc[0].to_dict()
                    vai("Home")
                else: st.error("Email o Password errati")
        with t2:
            er = st.text_input("La tua Email", key="r_e")
            pr = st.text_input("Scegli Password", type="password", key="r_p")
            if st.button("CREA ACCOUNT"):
                if er in df['email'].values: st.error("Utente già registrato")
                elif len(pr) < 4: st.error("Password troppo corta")
                else:
                    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                    nuovo = pd.DataFrame([{"email": er, "password": str(pr), "nome genitore": "Mamma", "nome bambino": "---", "taglia": "---", "data inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad}])
                    salva_dati(pd.concat([df, nuovo], ignore_index=True))
                    st.success("Account creato! Ora puoi accedere.")
else:
    # --- LOGICA AVVISI ---
    scadenza_str = str(st.session_state.dati_utente.get('scadenza', ''))
    if scadenza_str and scadenza_str != 'nan':
        try:
            giorni = (datetime.strptime(scadenza_str, "%Y-%m-%d") - datetime.now()).days
            if 0 <= giorni <= 10:
                st.markdown(f'<div class="avviso-scadenza">⚠️ Mancano {giorni} giorni al cambio Box!</div>', unsafe_allow_html=True)
        except: pass

    if st.session_state.pagina == "Home":
        st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
        st.markdown(f"### Ciao {st.session_state.dati_utente.get('nome genitore', 'Mamma')}! 👋")
        if img: st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:20px;">', unsafe_allow_html=True)
        if st.button("Logout"): 
            st.session_state.user = None
            vai("Welcome")

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.dati_utente.get('nome genitore', ''))
            nb = st.text_input("Bimbo", st.session_state.dati_utente.get('nome bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA DATI"):
                df.loc[df['email'] == st.session_state.user, ['nome genitore', 'nome bambino', 'taglia']] = [n, nb, tg]
                salva_dati(df)
                st.session_state.dati_utente['nome genitore'] = n
                st.success("Dati aggiornati sul foglio Google!")

    # --- NAV BAR ---
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📦", "Box"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag)
