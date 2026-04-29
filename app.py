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
                # Pulizia automatica nomi colonne
                df.columns = [str(c).strip() for c in df.columns]
                return df
        return pd.DataFrame()
    except: return pd.DataFrame()

def aggiungi_utente(nuovo):
    res = requests.post(API_URL, json={"data": [nuovo]})
    if res.status_code != 201:
        st.error(f"Errore Excel: {res.text}")
    return res.status_code

def aggiorna_utente(email, dati):
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati})

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

# --- 3. CSS TOTALE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; background-position: center; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 35px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; }} .box-sole {{ background-color: #FFD600 !important; color: #000 !important; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 20px; border: 1px solid #f87171; font-weight: 800; margin: 15px; text-align: center; }}
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
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"):
                    if not df_globale.empty:
                        # Cerchiamo con i nomi colonna puliti
                        m = df_globale[(df_globale['email'].str.lower() == e.lower()) & (df_globale['password'].astype(str) == str(p))]
                        if not m.empty:
                            st.session_state.user = m.iloc[0].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
                    else: st.error("Database in aggiornamento...")
        with t2:
            with st.form("r"):
                er, pr = st.text_input("Tua Email"), st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"):
                    # Mandiamo i dati con le chiavi ESATTE del foglio
                    scad = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                    nuovo = {"email": er, "password": str(pr), "nome genitore": "Mamma", "nome bambino": "---", "taglia": "---", "data inizio": datetime.now().strftime("%Y-%m-%d"), "scadenza": scad}
                    if aggiungi_utente(nuovo) == 201:
                        st.success("Registrato! Ora fai il login.")
else:
    # --- APP DOPO LOGIN ---
    scad_v = str(st.session_state.user.get('scadenza', ''))
    if scad_v != 'nan' and scad_v != '':
        try:
            gg = (datetime.strptime(scad_v, "%Y-%m-%d") - datetime.now()).days
            if 0 <= gg <= 10:
                st.markdown(f'<div class="avviso-scadenza">⚠️ Mancano {gg} giorni al cambio Box!</div>', unsafe_allow_html=True)
        except: pass

    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;"><div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; font-weight:600; color:#334155;">Il tuo armadio circolare.</div></div><div>{img_h}</div></div>""", unsafe_allow_html=True)
        if st.button("Esci"): st.session_state.user = None; vai("Welcome")

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Il tuo Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.user.get('nome genitore', ''))
            nb = st.text_input("Nome Bambino", st.session_state.user.get('nome bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA SU EXCEL"):
                aggiorna_utente(st.session_state.user['email'], {"nome genitore": n, "nome bambino": nb, "taglia": tg})
                st.session_state.user.update({"nome genitore": n, "nome bambino": nb, "taglia": tg})
                st.success("Sincronizzato!")

    # NAV BAR 7 COLONNE
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
