import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE (IL TUO FOGLIO)
# ==========================================
API_URL = "https://sheetdb.io"
SHEET_ID = "14mSfOS3lPs5_EdCEKwBGvhDIKnU-H5quZUk5e31X5s8"
# Metodo di emergenza per leggere se l'API dorme
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

def carica_db():
    try:
        # Proviamo prima l'API (più veloce per i nuovi dati)
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=5)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        # Se l'API fallisce, leggiamo il CSV diretto da Google
        df_alt = pd.read_csv(CSV_URL)
        df_alt.columns = [str(c).strip().lower() for c in df_alt.columns]
        return df_alt
    except:
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])

def registra_user(dati):
    requests.post(API_URL, json={"data": [dati]})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ==========================================
# 2. CONFIGURAZIONE PAGINA & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"n": nome, "p": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# ==========================================
# 3. DESIGN CSS (IL LOOK DI IERI 23:30)
# ==========================================
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img_data, logo_bg = get_base64("bimbo.jpg"), get_base64("logo.png")

st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}

    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 140px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 40px 40px; box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }}
    .header-text {{ color: white; font-size: 36px; font-weight: 800; letter-spacing: 4px; text-transform: uppercase; text-shadow: 2px 2px 15px rgba(0,0,0,0.5); }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 25px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 55px; font-size: 16px; box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
    }}
    
    .card {{ border-radius: 30px; padding: 25px; margin: 10px 10px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 12px 35px rgba(0,0,0,0.04); }}
    .box-luna {{ background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important; border: 1px solid #cbd5e1 !important; }}
    .box-sole {{ background: linear-gradient(135deg, #FFD600 0%, #FFB800 100%) !important; color: #1e293b !important; border: none !important; }}
    .prezzo-rosa {{ color: #f43f5e; font-size: 28px; font-weight: 900; margin: 10px 0; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 20px; background: #FFFFFF; border-radius: 25px; margin-bottom: 15px; border-left: 8px solid #f43f5e; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA ACCESSO
# ==========================================
df_db = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Vestili bene, falli crescere bene. 🔄</h2>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; padding: 10px 40px; color:#64748b;'>Il primo abbonamento di abbigliamento circolare per neonati.</div>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")

    elif st.session_state.pagina == "Login":
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        with tab1:
            with st.form("l"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_db.empty:
                        hp = hash_password(p)
                        # Pulizia password excel (.0)
                        df_db['p_clean'] = df_db['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        match = df_db[(df_db['email'].astype(str).str.lower() == e) & (df_db['p_clean'] == hp)]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati")
                    else: st.error("Database non raggiungibile. Controlla la connessione!")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Scegli Password", type="password")
                rn = st.text_input("Nome Genitore")
                rb = st.text_input("Nome Bambino")
                rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                rl = st.selectbox("Punto di ritiro", ["Locker Milano", "Locker Roma", "Locker Torino", "InPost Locker"])
                if st.form_submit_button("CREA ACCOUNT"):
                    if re and rp:
                        nuovo = {"email": re.strip().lower(), "password": hash_password(rp), "nome_genitore": rn, "nome_bambino": rb, "taglia": rt, "data_inizio": str(date.today()), "scadenza": "", "locker": rl}
                        registra_user(nuovo)
                        st.success("Registrato! Ora fai l'Accedi.")
                        st.balloons()

# ==========================================
# 5. APP DOPO LOGIN
# ==========================================
else:
    # --- NAV BAR FISSA (7 ICONE) ---
    c_nav = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
    st.divider()

    # --- HOME (GRIGLIA) ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:35px;">' if img_data else ""
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; padding: 0 10px; align-items: start;">
            <div>
                <div style="font-size:34px; font-weight:800; color:#1e293b; line-height:1.1;">Ciao {nome}! 👋</div>
                <div style="font-size:16px; color:#475569; margin-top:15px;">Il tuo armadio circolare è pronto.</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #f43f5e; margin-top:30px;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

    # --- INFO ---
    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""<div class="info-box"><b>🚚 LOCKER:</b> Box in 3-5 giorni. Ritira 24/7.</div>
        <div class="info-box"><b>🔄 CAMBIO:</b> Ordina la taglia nuova e rendi la vecchia insieme.</div>""", unsafe_allow_html=True)

    # --- BOX ---
    elif st.session_state.pagina == "Box":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="card box-luna"><h3>LUNA 🌙</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button("Scegli Luna"): aggiungi("Box Luna 🌙", 19.90)
        with col2:
            st.markdown(f'<div class="card box-sole"><h3>SOLE ☀️</h3><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button("Scegli Sole"): aggiungi("Box Sole ☀️", 19.90)

    # --- CHI SIAMO ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.7;">Siamo genitori che hanno detto basta allo spreco. Abbiamo creato LoopBaby per far viaggiare la qualità di famiglia in famiglia.🌿</div>', unsafe_allow_html=True)

    # --- PROFILO ---
    elif st.session_state.pagina == "Profilo":
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Nome:</b> {u.get('nome_genitore')}<br>
            <b>📏 Taglia:</b> {u.get('taglia')}<br>
            <b>📍 Locker:</b> {u.get('locker')}
        </div>""", unsafe_allow_html=True)
        if st.button("Logout"): st.session_state.user = None; vai("Welcome")
