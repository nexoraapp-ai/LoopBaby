import streamlit as st
import pandas as pd
import urllib.request
import json
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (SISTEMA ANTI-BOT) ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Per leggere usiamo un URL pulito per evitare conflitti
        with urllib.request.urlopen(f"{API_URL}?t={datetime.now().microsecond}") as response:
            data = json.loads(response.read().decode())
            if data:
                df = pd.DataFrame(data)
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])
    except:
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])

def invia_dati(payload, metodo='POST', endpoint=API_URL):
    # Simula perfettamente ReqBin per evitare il 405
    req = urllib.request.Request(endpoint, method=metodo)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0') # Si finge un browser umano
    
    jsondata = json.dumps({"data": [payload]}).encode('utf-8')
    try:
        with urllib.request.urlopen(req, data=jsondata) as f:
            return f.getcode()
    except urllib.error.HTTPError as e:
        return e.code

# --- 2. CONFIGURAZIONE E STATO ---
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
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 35px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; border: none !important; height: 45px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    .accent {{ color: #f43f5e; font-weight: 800; font-size: 11px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ---
df_globale = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty:
                        df_globale['e_c'] = df_globale['email'].astype(str).str.strip().str.lower()
                        df_globale['p_c'] = df_globale['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        m = df_globale[(df_globale['e_c'] == e) & (df_globale['p_c'] == p)]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati.")
                    else: st.warning("Database in aggiornamento... Riprova.")
        with t2:
            with st.form("r"):
                er = st.text_input("Email")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if er and pr:
                        scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                        nuovo = {"email": er.strip(), "password": pr.strip(), "nome": "Mamma", "taglia": "---", "inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad, "locker": "Non impostato"}
                        status = invia_dati(nuovo)
                        if status == 201:
                            st.success("✅ REGISTRATA! Ora fai l'accesso.")
                            st.balloons()
                        else: st.error(f"Errore tecnico {status}. SheetDB ha rifiutato la richiesta.")

else:
    # --- APP DOPO LOGIN ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio infinito è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        if st.button("Logout"): 
            st.session_state.user = None; vai("Welcome")

    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida al Servizio 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""<div class="info-box"><span class="accent">🚚 LOCKER INPOST</span><br>Ritira la Box 24/7 nel locker più vicino.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE</span><br>Ogni capo viene sanificato professionalmente ad alte temperature.</div>""", unsafe_allow_html=True)

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Il tuo Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.user.get('nome'))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            loc = st.text_input("Locker InPost preferito", st.session_state.user.get('locker'))
            if st.form_submit_button("SALVA"):
                invia_dati({"nome": n, "taglia": tg, "locker": loc}, metodo='PATCH', endpoint=f"{API_URL}/email/{st.session_state.user['email']}")
                st.session_state.user.update({"nome": n, "taglia": tg, "locker": loc})
                st.success("Sincronizzato!")

    # NAVIGAZIONE FISSA
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    m_list = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(m_list):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag)
