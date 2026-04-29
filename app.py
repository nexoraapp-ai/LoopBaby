import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
from datetime import date, datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE ---
API_URL = "https://sheetdb.io"

def carica_db():
    try:
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
    requests.post(API_URL, json={"data": [dati]})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 2. CONFIGURAZIONE PAGINA & STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# --- 3. IMMAGINI E STILE ---
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; }}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; height: 45px;
    }}

    .card {{ border-radius: 25px; padding: 20px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); margin-bottom: 15px; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 22px; font-weight: 900; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO ---
df = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")

    elif st.session_state.pagina == "Login":
        with st.form("login"):
            e = st.text_input("Email").strip().lower()
            p = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                if not df.empty:
                    m = df[(df['email'].str.lower() == e) & (df['password'] == hash_password(p))]
                    if not m.empty:
                        st.session_state.user = m.iloc[-1].to_dict()
                        vai("Home")
                    else: st.error("Dati errati")
        st.button("Sei nuova? Registrati", on_click=lambda: vai("Registrazione"))

    elif st.session_state.pagina == "Registrazione":
        with st.form("reg"):
            email = st.text_input("Email")
            psw = st.text_input("Password", type="password")
            nome = st.text_input("Nome genitore")
            bimbo = st.text_input("Nome bambino")
            taglia = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            locker = st.selectbox("Locker InPost", ["Milano Centro", "Roma Termini", "Torino Porta Nuova"])
            if st.form_submit_button("CREA ACCOUNT"):
                nuovo = {"email": email.strip().lower(), "password": hash_password(psw), "nome": nome, "bimbo": bimbo, "taglia": taglia, "inizio": str(date.today()), "scadenza": str(date.today() + timedelta(days=90)), "locker": locker}
                registra_user(nuovo)
                st.success("Registrato! Fai il login.")
                vai("Login")

# --- 5. APP LOGGED IN ---
else:
    # --- NAV BAR 7 ICONE ---
    c = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag)

    # --- PAGINA HOME (GRIGLIA AVANZATA) ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        n = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:26px; font-weight:800;">Ciao {n}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio infinito è pronto.</div></div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

    # --- CHI SIAMO (EMOZIONALE) ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("## La nostra Storia ❤️")
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">'
                    '<b>Ma quanto è brutto quando quella tutina che ami non entra più?</b><br><br>'
                    'LoopBaby nasce per eliminare lo spreco e far viaggiare i vestiti di famiglia in famiglia. '
                    'Insieme, proteggiamo il pianeta dei nostri figli. 🌿</div>', unsafe_allow_html=True)

    # --- BOX (COLORATE) ---
    elif st.session_state.pagina == "Box":
        st.markdown("## Scegli Box 📦")
        for s, c, p in [("LUNA 🌙", "#f1f5f9", 19.90), ("SOLE ☀️", "#FFD600", 19.90)]:
            st.markdown(f'<div class="card" style="background:{c};"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}"): aggiungi_al_carrello(f"Box {s}", p)

    # ... (le altre pagine Profilo/Carrello/Info seguono lo stesso stile)
