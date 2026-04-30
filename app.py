import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# --- 1. FUNZIONI DATABASE & SICUREZZA (SHEETDB) ---
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
    # La funzione che salva direttamente su Excel via SheetDB
    requests.post(API_URL, json={"data": [dati]})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(nome_pag): 
    st.session_state.pagina = nome_pag

def aggiungi_al_carrello(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

img_data = get_base64("bimbo.jpg")
logo_bg = get_base64("logo.png") 

# --- 3. CSS TOTALE (Design Originale Integrale) ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
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
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; height: 45px; border: none !important;
    }}

    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .link-inline {{ color: #475569 !important; font-weight: 800 !important; text-decoration: underline !important; cursor: pointer; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO ---
df_db = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login"); st.rerun()

    elif st.session_state.pagina == "Login":
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        with tab1:
            with st.form("l"):
                e = st.text_input("Email").strip().lower()
                p = st.text_input("Password", type="password").strip()
                if st.form_submit_button("ENTRA"):
                    if not df_db.empty:
                        hp = hash_password(p)
                        df_db['pass_fix'] = df_db['password'].astype(str).str.replace('.0','',regex=False).str.strip()
                        m = df_db[(df_db['email'].str.lower() == e) & (df_db['pass_fix'] == hp)]
                        if not m.empty:
                            st.session_state.user = m.iloc[-1].to_dict()
                            vai("Home"); st.rerun()
                        else: st.error("Email o Password errati")
        with tab2:
            with st.form("r"):
                re = st.text_input("Email")
                rp = st.text_input("Password", type="password")
                rn = st.text_input("Nome genitore")
                rb = st.text_input("Nome bambino")
                rt = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
                rl = st.selectbox("Locker", ["InPost", "Esselunga", "Poste Italiane"])
                if st.form_submit_button("Crea account"):
                    nuovo = {"email": re.strip().lower(), "password": hash_password(rp), "nome_genitore": rn, "nome_bambino": rb, "taglia": rt, "data_inizio": str(date.today()), "scadenza": "", "locker": rl}
                    registra_user(nuovo)
                    st.success("Registrato! Ora fai l'accesso."); st.balloons()

else:
    # --- BARRA NAVIGAZIONE FISSA (7 COLONNE) ---
    st.markdown('<div style="margin-top:-30px;"></div>', unsafe_allow_html=True)
    cols = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with cols[i]:
            label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
            if st.button(label, key=f"n_{pag}"): vai(pag); st.rerun()
    st.divider()

    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        img_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        u_nome = st.session_state.user.get('nome_genitore', 'Mamma')
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
            <div>
                <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_nome}! 👋</div>
                <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino.</div>
                <div style="margin-top:15px;">
                    <div style="font-size:11px; color:#475569; margin-bottom:8px;">👶 Capi di qualità selezionati</div>
                    <div style="font-size:11px; color:#475569; margin-bottom:8px;">🔄 Cambi quando cresce</div>
                </div>
            </div>
            <div>{img_html}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48;">✨ Promo Fondatrici</b><br><p style="font-size:13px; margin-top:5px;">Dona 10 capi e ricevi una <b>BOX OMAGGIO</b>!</p></div>""", unsafe_allow_html=True)

    elif st.session_state.pagina == "Info":
        st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
        st.markdown("""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
            <b>1. Scegli e Ricevi:</b> Scegli la tua Box e ricevila nel Locker scelto.<br><br>
            <b>2. Controllo Qualità:</b> Hai 48 ore per controllare i capi.<br><br>
            <b>🚚 Spedizioni:</b> Se continui il ciclo, paghiamo noi andata e ritorno!</div>""", unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center;">Il Patto del 10 📍</h2>', unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; font-size:13px;"><b>♻️ Equilibrio:</b> Rendi 10 capi per riceverne 10 nuovi.</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "Box":
        tg_u = st.session_state.user.get('taglia', '50-56 cm')
        st.markdown(f'<div style="text-align:center;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700;">📍 TAGLIA: {tg_u}</span></div>', unsafe_allow_html=True)
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): aggiungi_al_carrello(f"Box {s}", 19.90)

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
        st.markdown("""<div style="padding: 0 20px; font-size:14px; color:#475569; line-height:1.6; text-align:center;">
            Ma quanto è brutto quando quella tutina che ami non entra più? LoopBaby nasce per dire basta a questo. 🛑
        </div>""", unsafe_allow_html=True)

    elif st.session_state.pagina == "Profilo":
        u = st.session_state.user
        st.markdown(f"""<div class="card" style="text-align:left;">
            <b>👤 Nome:</b> {u.get('nome_genitore')}<br>
            <b>👶 Bimbo:</b> {u.get('nome_bambino')}<br>
            <b>📍 Locker:</b> {u.get('locker')}</div>""", unsafe_allow_html=True)
        if st.button("LOGOUT"): st.session_state.user = None; vai("Welcome"); st.rerun()

    elif st.session_state.pagina == "Carrello":
        st.markdown('<h2 style="text-align:center;">Carrello 🛒</h2>', unsafe_allow_html=True)
        if not st.session_state.carrello: st.write("Vuoto.")
        else:
            totale = sum(item['prezzo'] for item in st.session_state.carrello)
            for item in st.session_state.carrello:
                st.write(f"✅ {item['nome']} - {item['prezzo']:.2f}€")
            st.markdown(f"<h3 style='text-align:right;'>Totale: {totale:.2f}€</h3>", unsafe_allow_html=True)
