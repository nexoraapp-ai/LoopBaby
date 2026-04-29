import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import base64
import os

# --- 1. CONFIGURAZIONE DATABASE (PULITA) ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        # Per LEGGERE usiamo il timestamp per non vedere dati vecchi
        t = datetime.now().strftime('%H%M%S')
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])
    except:
        return pd.DataFrame(columns=['email', 'password', 'nome', 'bimbo', 'taglia', 'inizio', 'scadenza', 'locker'])

def aggiungi_utente(nuovo):
    # PER SCRIVERE: URL pulito, niente parametri extra. Identico a ReqBin.
    res = requests.post(API_URL, json={"data": [nuovo]}, timeout=15)
    return res.status_code

def aggiorna_utente(email, dati_agg):
    # Aggiornamento riga specifica
    res = requests.patch(f"{API_URL}/email/{email}", json={"data": dati_agg})
    return res.status_code

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

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
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; height: 45px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
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
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty:
                        df_globale['p_c'] = df_globale['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        m = df_globale[(df_globale['email'].str.lower() == e) & (df_globale['p_c'] == p)]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Dati errati.")
        with t2:
            with st.form("r"):
                er = st.text_input("Email")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    if er and pr:
                        with st.spinner("Registrazione..."):
                            scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                            nuovo = {"email": er.strip(), "password": pr.strip(), "nome": "Mamma", "bimbo": "---", "taglia": "---", "inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad, "locker": "Da definire"}
                            status = aggiungi_utente(nuovo)
                        if status == 201:
                            st.success("✅ REGISTRATA! Ora puoi accedere.")
                            st.balloons()
                        else: st.error(f"Errore {status}. Riprova tra 10 secondi.")

else:
    # --- APP DOPO LOGIN ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        n = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
            <div><div style="font-size:28px; font-weight:800;">Ciao {n}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; vai("Welcome")

    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida 🔄</h2>", unsafe_allow_html=True)
        st.markdown('<div class="info-box"><span class="accent">🚚 Locker InPost</span><br>Consegna in 3-5 giorni. Ritira quando vuoi 24/7.</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        with st.form("p"):
            nome = st.text_input("Nome", st.session_state.user.get('nome', ''))
            loc = st.text_input("Locker preferito", st.session_state.user.get('locker', ''))
            if st.form_submit_button("SALVA"):
                aggiorna_utente(st.session_state.user['email'], {"nome": nome, "locker": loc})
                st.session_state.user.update({"nome": nome, "locker": loc})
                st.success("Dati salvati!")

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>Chi Siamo ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">Siamo genitori stanchi dello spreco. Abbiamo creato LoopBaby per far viaggiare la qualità di famiglia in famiglia.🌿</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE FISSA (6 ICONE)
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    m_list = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(m_list):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag)
