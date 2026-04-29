import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE & SICUREZZA
# ==========================================
API_URL = "https://sheetdb.io"

def carica_db():
    try:
        t = datetime.now().microsecond
        res = requests.get(f"{API_URL}?t={t}", timeout=10)
        if res.status_code == 200:
            df = pd.DataFrame(res.json())
            if not df.empty:
                # Forza nomi colonne minuscoli per il codice
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except: return pd.DataFrame()

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

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"n": nome, "p": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# ==========================================
# 3. DESIGN CSS (QUELLO DI IERI SERA)
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
        margin-bottom: 35px; border-radius: 0 0 35px 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 34px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); }}

    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 20px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important;
        border: none !important; height: 50px; font-size: 16px; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2);
    }}

    .card {{ border-radius: 25px; padding: 22px; margin: 10px 15px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.03); margin-bottom: 15px; }}
    .box-luna {{ background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%) !important; }}
    .box-sole {{ background: linear-gradient(135deg, #FFD600 0%, #FFB800 100%) !important; color: black !important; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; margin-top: 10px; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 18px; background: #FFFFFF; border-radius: 20px; margin-bottom: 15px; border-left: 6px solid #f43f5e; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. LOGICA ACCESSO
# ==========================================
df_db = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px; color:#64748b;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
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
                        # Fix password: toglie .0 che Excel mette ai numeri
                        df_db['p_fix'] = df_db['password'].astype(str).str.replace('.0','',regex=False).str.strip()
                        match = df_db[(df_db['email'].str.lower() == e) & (df_db['p_fix'] == hp)]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Email o Password errati")
                    else: st.warning("Database in caricamento... Riprova.")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Scegli Password", type="password")
                rn = st.text_input("Nome Genitore")
                rb = st.text_input("Nome Bambino")
                rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                rl = st.selectbox("Locker preferito", ["InPost", "Esselunga", "Poste Italiane"])
                if st.form_submit_button("CREA ACCOUNT"):
                    if re and rp:
                        nuovo = {
                            "email": re.strip().lower(),
                            "password": hash_password(rp),
                            "nome_genitore": rn,
                            "nome_bambino": rb,
                            "taglia": rt,
                            "data_inizio": str(date.today()),
                            "scadenza": str(date.today() + timedelta(days=90)),
                            "locker": rl
                        }
                        registra_user(nuovo)
                        st.success("Registrato! Ora fai l'Accedi.")
                        st.balloons()

# ==========================================
# 5. APP DOPO IL LOGIN (THE FULL VERSION)
# ==========================================
else:
    # --- NAV BAR FISSA (7 ICONE) ---
    c_nav = st.columns(7)
    icons = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(icons):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
    st.divider()

    # --- HOME (GRIGLIA AVANZATA) ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:30px; box-shadow:0 10px 25px rgba(0,0,0,0.1);">' if img_data else ""
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 15px; padding: 0 10px; align-items: center;">
            <div>
                <div style="font-size:30px; font-weight:800; color:#1e293b; line-height:1.1;">Ciao {nome}! 👋</div>
                <div style="font-size:15px; color:#475569; margin-top:10px;">Il tuo armadio circolare è pronto.</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #f43f5e; margin-top:25px;">'
                    '<b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Scopri di più"): vai("Info")

    # --- INFO ---
    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 CONSEGNA</span><br>Box spedita in 24h. Arriva in 3-5 giorni nel Locker scelto.</div>
        <div class="info-box"><span class="accent">🔄 CAMBIO TAGLIA</span><br>Quando i vestiti stringono, ordina la taglia nuova. Consegniamo la nuova e ritiri la vecchia.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE</span><br>Sanificazione professionale ad alte temperature per ogni capo.</div>
        """, unsafe_allow_html=True)

    # --- BOX ---
    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Le Box 📦</h2>", unsafe_allow_html=True)
        for s, c, p in [("LUNA 🌙", "box-luna", 19.90), ("SOLE ☀️", "box-sole", 19.90)]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi(s, p)

    # --- PROFILO ---
    elif st.session_state.pagina == "Profilo":
        st.markdown("<h2 style='text-align:center;'>Profilo 👤</h2>", unsafe_allow_html=True)
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Nome:</b> {u.get('nome_genitore')}<br>
            <b>👶 Bambino:</b> {u.get('nome_bambino')}<br>
            <b>📏 Taglia:</b> {u.get('taglia')}<br>
            <b>📅 Inizio:</b> {u.get('data_inizio')}<br>
            <b>📍 Locker:</b> {u.get('locker')}
        </div>""", unsafe_allow_html=True)
        if st.button("LOGOUT"): st.session_state.user = None; vai("Welcome")

    # --- CARRELLO ---
    elif st.session_state.pagina == "Carrello":
        st.markdown("<h2 style='text-align:center;'>Carrello 🛒</h2>", unsafe_allow_html=True)
        if not st.session_state.carrello: st.write("Vuoto.")
        else:
            tot = sum(i['p'] for i in st.session_state.carrello)
            for i in st.session_state.carrello: st.write(f"✅ {i['n']} - {i['p']}€")
            st.markdown(f"### Totale: {tot:.2f}€")
            if st.button("PAGA ORA"): st.info("Link Stripe in arrivo...")

    # --- CHI SIAMO ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>Chi Siamo ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">Siamo genitori stanchi dello spreco. Abbiamo creato LoopBaby per far viaggiare la qualità di famiglia in famiglia.🌿</div>', unsafe_allow_html=True)

    # --- SHOP ---
    elif st.session_state.pagina == "Shop":
        st.markdown("<h2 style='text-align:center;'>Shop 🛍️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio Loop Love</b><br><div class="prezzo-rosa">9,90€</div></div>', unsafe_allow_html=True)
        if st.button("Aggiungi Extra"): aggiungi("Body Bio", 9.90)
