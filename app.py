import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
from datetime import date, datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE ---
API_URL = "https://sheetdb.io/api/v1/ju68nzk8x69ta"

def carica_db():
    try:
        # Cache buster per leggere sempre dati nuovi
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame()
    except: return pd.DataFrame()

def registra_user(dati):
    # La funzione che salva direttamente su Excel via SheetDB
    requests.post(API_URL, json={"data": [dati]})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

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
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; border-radius: 0 0 30px 30px; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 20px !important; width: 100% !important; font-weight: 800 !important; border: none !important; height: 45px; }}
    .card {{ border-radius: 25px; padding: 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO (LOGIN / REGISTRAZIONE) ---
df = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 20px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")

    elif st.session_state.pagina == "Login":
        st.markdown('<h2 style="text-align:center;">Accedi ✨</h2>', unsafe_allow_html=True)
        with st.form("login_form"):
            e = st.text_input("Email").strip().lower()
            p = st.text_input("Password", type="password").strip()
            if st.form_submit_button("ENTRA"):
                if not df.empty:
                    hp = hash_password(p)
                    user_match = df[(df['email'].str.lower() == e) & (df['password'] == hp)]
                    if not user_match.empty:
                        st.session_state.user = user_match.iloc[-1].to_dict()
                        vai("Home")
                    else: st.error("Email o Password errati")
                else: st.error("Nessun utente registrato.")
        if st.button("Non hai un account? Registrati"): vai("Registrazione")

    elif st.session_state.pagina == "Registrazione":
        st.markdown('<h2 style="text-align:center;">Registrati ✨</h2>', unsafe_allow_html=True)
        with st.form("reg_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            nome = st.text_input("Nome genitore")
            bambino = st.text_input("Nome bambino")
            taglia = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            locker = st.selectbox("Locker preferito", ["InPost", "Esselunga", "Poste Italiane"])
            
            if st.form_submit_button("Crea account"):
                if email and password:
                    nuovo = {
                        "email": email.strip().lower(),
                        "password": hash_password(password),
                        "nome": nome, # Mappato su colonna 'nome' di Excel
                        "bimbo": bambino,
                        "taglia": taglia,
                        "inizio": str(date.today()),
                        "scadenza": str(date.today() + timedelta(days=90)),
                        "locker": locker
                    }
                    registra_user(nuovo)
                    st.success("Account creato con successo!")
                    vai("Login")
                else: st.warning("Compila i campi obbligatori.")
        if st.button("Torna al Login"): vai("Login")

# --- 5. APP DOPO IL LOGIN ---
else:
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome_mamma = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div>
                <div style="font-size:26px; font-weight:800;">Ciao {nome_mamma}! 👋</div>
                <div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div>
            </div>
            <div>{img_h}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout"): 
            st.session_state.user = None
            vai("Welcome")

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("## La nostra Storia ❤️")
        st.markdown('<div class="card" style="text-align:left;">Siamo genitori stanchi dello spreco. Abbiamo creato LoopBaby per far viaggiare la qualità di famiglia in famiglia.🌿</div>', unsafe_allow_html=True)

    # --- BARRA NAVIGAZIONE FISSA ---
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📖", "Info"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
