import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONNESSIONE GOOGLE SHEETS ---
URL_FOGLIO = "https://google.com"

conn = st.connection("gsheets", type=GSheetsConnection)

def carica_dati():
    return conn.read(spreadsheet=URL_FOGLIO, usecols=[0,1,2,3,4,5,6])

def salva_dati(df_nuovo):
    conn.update(spreadsheet=URL_FOGLIO, data=df_nuovo)
    st.cache_data.clear()

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def get_b64(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img, logo = get_b64("bimbo.jpg"), get_b64("logo.png")

# --- 3. STILE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7; max-width: 450px; margin: 0 auto; padding-bottom: 100px; }}
    .header {{ background-image: linear-gradient(rgba(0,0,0,0.1),rgba(0,0,0,0.1)), url("data:image/png;base64,{logo}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 20px; }}
    .header-t {{ color: white; font-size: 30px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background: #f43f5e !important; color: white !important; border-radius: 15px; width: 100%; font-weight: 700; border: none; }}
    .card {{ border-radius: 20px; padding: 20px; margin: 10px; border: 1px solid #EAE2D6; background: white; }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 15px; border: 1px solid #f87171; font-weight: 700; text-align: center; margin: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df = carica_dati()

if st.session_state.user is None:
    st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            user_row = df[(df['email'] == e) & (df['password'] == p)]
            if not user_row.empty:
                st.session_state.user = e
                st.session_state.dati_utente = user_row.iloc[0].to_dict()
                vai("Home")
            else: st.error("Email o Password errati")
            
    with t2:
        er = st.text_input("Email ")
        pr = st.text_input("Password ", type="password")
        if st.button("CREA ACCOUNT"):
            if er in df['email'].values: st.error("Utente già registrato")
            else:
                nuovo_rigo = pd.DataFrame([{"email": er, "password": pr, "nome_genitore": "Mamma", "taglia": "---", "data_inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")}])
                salva_dati(pd.concat([df, nuovo_rigo], ignore_index=True))
                st.success("Registrazione completata! Ora accedi.")

else:
    # --- LOGICA AVVISI SCADENZA ---
    scadenza_str = st.session_state.dati_utente.get('scadenza', '')
    if scadenza_str:
        giorni_mancanti = (datetime.strptime(scadenza_str, "%Y-%m-%d") - datetime.now()).days
        if giorni_mancanti <= 10:
            st.markdown(f'<div class="avviso-scadenza">⚠️ ATTENZIONE: Mancano {max(0, giorni_mancanti)} giorni al cambio Box! Prenota ora la nuova taglia.</div>', unsafe_allow_html=True)

    if st.session_state.pagina == "Home":
        st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
        st.markdown(f"### Ciao {st.session_state.dati_utente['nome_genitore']}! 👋")
        if img: st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:20px;">', unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; st.rerun()

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.dati_utente['nome_genitore'])
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA SUL FOGLIO GOOGLE"):
                df.loc[df['email'] == st.session_state.user, ['nome_genitore', 'taglia']] = [n, tg]
                salva_dati(df)
                st.session_state.dati_utente['nome_genitore'] = n
                st.success("Dati salvati!")

    # NAV
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    with c[0]: 
        if st.button("🏠"): vai("Home")
    with c[1]: 
        if st.button("📦"): vai("Box")
    with c[2]: 
        if st.button("👤"): vai("Profilo")
    with c[3]: 
        if st.button("👋"): vai("ChiSiamo")
