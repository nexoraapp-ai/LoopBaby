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
                df.columns = [str(c).strip().lower() for c in df.columns]
                return df
        return pd.DataFrame(columns=['email','password','nome_genitore','nome_bambino','taglia','data_inizio','scadenza','locker'])
    except: return pd.DataFrame()

def registra_user(dati):
    requests.post(API_URL, json={"data": [dati]})

def aggiorna_user(email, dati):
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati})

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

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"n": nome, "p": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# ==========================================
# 3. IMMAGINI E DESIGN CSS (REALE 23:30)
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
        transition: all 0.3s ease;
    }}
    
    .card {{ border-radius: 30px; padding: 25px; margin: 10px 10px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 12px 35px rgba(0,0,0,0.04); }}
    .box-luna {{ background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important; border: 1px solid #cbd5e1 !important; }}
    .box-sole {{ background: linear-gradient(135deg, #FFD600 0%, #FFB800 100%) !important; color: #1e293b !important; border: none !important; }}
    .prezzo-rosa {{ color: #f43f5e; font-size: 28px; font-weight: 900; margin: 10px 0; }}
    
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.6; padding: 20px; background: #FFFFFF; border-radius: 25px; margin-bottom: 15px; border-left: 8px solid #f43f5e; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    .nav-bar {{ position: fixed; bottom: 0; left: 0; width: 100%; background: white; padding: 15px 0; border-top: 1px solid #EEE; display: flex; justify-content: space-around; z-index: 1000; }}
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
        st.markdown("<div style='text-align:center; padding: 10px 40px; color:#64748b;'>Il primo abbonamento di abbigliamento circolare per neonati in Italia.</div>", unsafe_allow_html=True)
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
                        df_db['p_clean'] = df_db['password'].astype(str).str.replace('.0', '', regex=False).str.strip()
                        match = df_db[(df_db['email'].str.lower() == e) & (df_db['p_clean'] == hp)]
                        if not match.empty:
                            st.session_state.user = match.iloc[-1].to_dict()
                            vai("Home")
                        else: st.error("Dati errati")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Scegli Password", type="password")
                rn = st.text_input("Nome Genitore")
                rb = st.text_input("Nome Bambino")
                rt = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                rl = st.selectbox("Punto di ritiro", ["Locker Milano", "Locker Roma", "Locker Torino", "Spedizione Casa"])
                if st.form_submit_button("CREA ACCOUNT"):
                    nuovo = {"email": re.strip().lower(), "password": hash_password(rp), "nome_genitore": rn, "nome_bambino": rb, "taglia": rt, "data_inizio": str(date.today()), "scadenza": str(date.today()+timedelta(days=90)), "locker": rl}
                    registra_user(nuovo)
                    st.success("Registrato! Ora fai l'Accedi.")
                    st.balloons()

# ==========================================
# 5. APP DOPO LOGIN
# ==========================================
else:
    # --- BARRA NAVIGAZIONE FISSA ---
    c_nav = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c_nav[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"nav_{pag}"): vai(pag)
    st.divider()

    # --- HOME ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.user.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:35px; box-shadow:0 15px 35px rgba(0,0,0,0.12);">' if img_data else ""
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; padding: 0 10px; align-items: start;">
            <div>
                <div style="font-size:34px; font-weight:800; color:#1e293b; line-height:1.1;">Ciao {nome}! 👋</div>
                <div style="font-size:16px; color:#475569; margin-top:15px; font-weight:300;">Benvenuta nel tuo armadio circolare.</div>
            </div>
            <div>{img_h}</div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #f43f5e; margin-top:30px;">'
                    '<b>🎁 PROMO MAMME FONDATRICI</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

    # --- INFO ---
    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Come funziona 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><span class="accent">1. ORDINA</span><br>Scegli la box della tua taglia attuale. Riceverai 10-12 capi igienizzati.</div>
        <div class="info-box"><span class="accent">2. USA</span><br>Tienili per tutto il tempo che serve. Non preoccuparti dell'usura quotidiana.</div>
        <div class="info-box"><span class="accent">3. SCAMBIA</span><br>Quando i vestiti stringono, ordina la taglia successiva. La nuova arriva, la vecchia torna a noi.</div>
        <div class="info-box"><span class="accent">4. LOGISTICA</span><br>Usiamo i Locker InPost 24/7 per non farti perdere tempo a casa.</div>
        """, unsafe_allow_html=True)

    # --- BOX ---
    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Scegli la tua Box 📦</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="card box-luna"><h3>LUNA 🌙</h3><div class="prezzo-rosa">19,90€</div><div style="font-size:12px;">Taglia 0-3 mesi</div></div>', unsafe_allow_html=True)
            if st.button("Aggiungi Luna"): aggiungi_al_carrello("Box Luna 🌙", 19.90)
        with col2:
            st.markdown(f'<div class="card box-sole"><h3>SOLE ☀️</h3><div class="prezzo-rosa">19,90€</div><div style="font-size:12px;">Taglia 3-6 mesi</div></div>', unsafe_allow_html=True)
            if st.button("Aggiungi Sole"): aggiungi_al_carrello("Box Sole ☀️", 19.90)

    # --- SHOP ---
    elif st.session_state.pagina == "Shop":
        st.markdown("<h2 style='text-align:center;'>Shop Extra 🛍️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card">👕 <b>Body Bio LoopLove (Set 3)</b><br><div class="prezzo-rosa">14,90€</div></div>', unsafe_allow_html=True)
        if st.button("Aggiungi Set 🎁"): aggiungi_al_carrello("Set Body Bio", 14.90)

    # --- PROFILO ---
    elif st.session_state.pagina == "Profilo":
        st.markdown("<h2 style='text-align:center;'>Tuo Profilo 👤</h2>", unsafe_allow_html=True)
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Mamma:</b> {u.get('nome_genitore')}<br>
            <b>👶 Bambino:</b> {u.get('nome_bambino')}<br>
            <b>📏 Taglia:</b> {u.get('taglia')}<br>
            <b>📅 Inizio:</b> {u.get('data_inizio')}<br>
            <b>📍 Punto Ritiro:</b> {u.get('locker')}
        </div>""", unsafe_allow_html=True)
        if st.button("Esci"): st.session_state.user = None; vai("Welcome")

    # --- CARRELLO ---
    elif st.session_state.pagina == "Carrello":
        st.markdown("<h2 style='text-align:center;'>Il tuo Carrello 🛒</h2>", unsafe_allow_html=True)
        if not st.session_state.carrello:
            st.warning("Il carrello è vuoto.")
        else:
            tot = sum(i['p'] for i in st.session_state.carrello)
            for i in st.session_state.carrello:
                st.write(f"✅ {i['n']} — {i['p']}€")
            st.markdown(f"<div style='text-align:right; font-size:26px; font-weight:900; color:#f43f5e;'>TOTALE: {tot:.2f}€</div>", unsafe_allow_html=True)
            if st.button("PAGA SICURO (STRIPE)"):
                st.success("Reindirizzamento...")

    # --- CHI SIAMO ---
    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.7;">'
                    'Siamo genitori che hanno detto basta allo spreco. '
                    'Abbiamo creato <b>LoopBaby</b> per dare vita a un armadio infinito dove i vestiti di qualità '
                    'viaggiano di casa in casa, seguendo la crescita dei più piccoli senza fermarsi in soffitta. 🌿</div>', unsafe_allow_html=True)
