import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
import json
from datetime import date, datetime, timedelta

# ==========================================
# 1. CONFIGURAZIONE DATABASE (SHEETDB)
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
    headers = {"Content-Type": "application/json"}
    requests.post(API_URL, json={"data": [dati]}, headers=headers)

def hash_psw(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ==========================================
# 2. CONFIGURAZIONE PAGINA & STATO
# ==========================================
st.set_page_config(page_title="LoopBaby", layout="centered", initial_sidebar_state="collapsed")

if "loggato" not in st.session_state: st.session_state.loggato = False
if "user_data" not in st.session_state: st.session_state.user_data = {}
if "pagina" not in st.session_state: st.session_state.pagina = "Home"
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

# ==========================================
# 3. CSS TOTALE (DESIGN ORIGINALE 23:30)
# ==========================================
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu {{display: none !important;}}
    @import url('https://googleapis.com');
    * {{ font-family: 'Lexend', sans-serif !important; }}
    .stApp {{ background-color: #FDFBF7 !important; max-width: 450px !important; margin: 0 auto !important; padding-bottom: 120px !important; }}
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; height: 48px; border: none !important; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 10px; border: 1px solid #EAE2D6; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); text-align: center; }}
    .box-luna {{ background-color: #f1f5f9 !important; border-color: #cbd5e1 !important; }}
    .box-sole {{ background-color: #FFD600 !important; border-color: #EAB308 !important; color: #000 !important; }} 
    .box-nuvola {{ background-color: #94A3B8 !important; border-color: #64748b !important; color: white !important; }}
    .box-premium {{ background: linear-gradient(135deg, #4F46E5 0%, #312E81 100%) !important; color: white !important; border: none; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .obiettivo-pink {{ background-color: #fff1f2; padding: 20px; border-radius: 20px; margin: 20px; text-align: center; border: 1px solid #fecdd3; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. SCHERMATA LOGIN BLOCCANTE
# ==========================================
if not st.session_state.loggato:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        with st.form("login"):
            e = st.text_input("Email").strip().lower()
            p = st.text_input("Password", type="password")
            if st.form_submit_button("ENTRA"):
                db = carica_db()
                if not db.empty:
                    db['p_fix'] = db['password'].astype(str).str.replace('.0','',regex=False).str.strip()
                    user = db[(db['email'].str.lower() == e) & (db['p_fix'] == hash_psw(p))]
                    if not user.empty:
                        st.session_state.loggato, st.session_state.user_data = True, user.iloc[-1].to_dict()
                        st.rerun()
                    else: st.error("Dati errati")
    with t2:
        with st.form("reg"):
            re, rp, rn = st.text_input("Email"), st.text_input("Password", type="password"), st.text_input("Tuo Nome")
            rt = st.selectbox("Taglia attuale", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("CREA ACCOUNT"):
                if re and rp:
                    registra_user({"email": re.strip().lower(), "password": hash_psw(rp), "nome_genitore": rn, "taglia": rt, "data_inizio": str(date.today())})
                    st.success("Registrato! Ora fai l'accesso.")
    st.stop()
    # ==========================================
# 5. APP DOPO LOGIN (THE FULL EXPERIENCE)
# ==========================================
st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)

# --- NAV BAR FISSA (7 ICONE) ---
st.markdown('<div style="margin-top:-30px;"></div>', unsafe_allow_html=True)
c_nav = st.columns(7)
menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
for i, (icon, pag) in enumerate(menu):
    with c_nav[i]:
        label = f"{icon}({len(st.session_state.carrello)})" if pag == "Carrello" and st.session_state.carrello else icon
        if st.button(label, key=f"nav_{pag}"): vai(pag)
st.divider()

# --- LOGICA PAGINE ---
if st.session_state.pagina == "Home":
    img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
    u_nome = st.session_state.user_data.get('nome_genitore', 'Mamma').split()[0]
    st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px; align-items: start;">
        <div>
            <div style="font-size:28px; font-weight:800; color:#1e293b;">Ciao {u_nome}! 👋</div>
            <div style="font-size:14px; font-weight:600; color:#334155; line-height:1.3;">L'armadio circolare che cresce con il tuo bambino: capi scelti con amore, per un futuro senza sprechi.</div>
            <div style="margin-top:15px;">
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px;">👶 Capi di qualità selezionati</div>
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569; margin-bottom:8px;">🔄 Cambi quando cresce</div>
                <div style="display:flex; align-items:center; gap:10px; font-size:11px; color:#475569;">💰 Risparmi oltre 1000€ l’anno</div>
            </div>
        </div>
        <div>{img_h}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="card" style="background-color: #FFF1F2; border: 2px dashed #F43F5E;"><b style="color:#E11D48; font-size:18px;">✨ Promo Mamme Fondatrici</b><br><p style="font-size:13px; color:#475569; margin-top:5px;">Dona almeno 10 capi e ricevi una <b>BOX OMAGGIO</b>! Trasporto a carico nostro.</p></div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Info":
    st.markdown('<h2 style="text-align:center;">Come funziona LoopBaby 🔄</h2>', unsafe_allow_html=True)
    st.markdown("""<div style="padding: 0 25px; font-size: 14px; color: #475569; line-height: 1.6;">
        <b>1. Scegli e Ricevi:</b> Nel Locker scelto.<br><br>
        <b>2. Controllo Qualità:</b> Hai 48 ore.<br><br>
        <b>3. Utilizzo:</b> Puoi tenere la Box per un massimo di 3 mesi.<br><br>
        <b>🚚 Spedizioni:</b> Se continui il ciclo, <b>paghiamo noi</b> andata e ritorno!</div>""", unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center;">Il Patto del 10 📍</h2>', unsafe_allow_html=True)
    st.markdown("""<div class="card" style="text-align:left; font-size:13px; color:#475569; line-height:1.6;">♻️ <b>Equilibrio:</b> Rendi 10 capi per riceverne 10 nuovi.<br><br>👖 <b>Sostituzione:</b> Se un capo si rovina, puoi sostituirlo o pagare 5€.</div>""", unsafe_allow_html=True)

elif st.session_state.pagina == "Box":
    tg_u = st.session_state.user_data.get('taglia', '50-56 cm')
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;"><span style="background:#e0f2f1; padding:5px 15px; border-radius:15px; font-size:12px; font-weight:700;">📍 CONFIGURATA PER: {tg_u}</span></div>', unsafe_allow_html=True)
    q = st.radio("Qualità:", ["Standard", "Premium"], horizontal=True)
    if q == "Standard":
        for s, c, d in [("LUNA 🌙", "box-luna", "Neutro"), ("SOLE ☀️", "box-sole", "Vivace")]:
            st.markdown(f'<div class="card {c}"><h3>{s}</h3><p>{d}</p><div class="prezzo-rosa">19,90€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): st.session_state.carrello.append({"n": s, "p": 19.90}); st.toast("Aggiunto!")
    else:
        st.markdown('<div class="card box-premium"><h3>BOX PREMIUM 💎</h3><p>Capi seminuovi di marca</p><div style="font-size:28px; font-weight:900;">29,90€</div></div>', unsafe_allow_html=True)
        if st.button("Scegli Premium"): st.session_state.carrello.append({"n": "Box Premium", "p": 29.90}); st.toast("Aggiunto!")

elif st.session_state.pagina == "Vetrina":
    st.markdown('<h2 style="text-align:center;">Shop 🛍️</h2>', unsafe_allow_html=True)
    st.markdown('<div class="card">👕 <b>Body Bio LoopLove</b><br><span class="prezzo-rosa">9,90€</span></div>', unsafe_allow_html=True)
    if st.button("Aggiungi Extra 🎁"): st.session_state.carrello.append({"n": "Body Bio", "p": 9.90}); st.toast("Aggiunto!")

elif st.session_state.pagina == "Profilo":
    u = st.session_state.user_data
    st.markdown(f"""<div class="card" style="text-align:left;"><b>👤 Nome:</b> {u.get('nome_genitore')}<br><b>📧 Email:</b> {u.get('email')}<br><b>📏 Taglia:</b> {u.get('taglia')}</div>""", unsafe_allow_html=True)
    if st.button("LOGOUT"): st.session_state.loggato = False; st.rerun()

elif st.session_state.pagina == "Carrello":
    st.markdown('<h2 style="text-align:center;">Carrello 🛒</h2>', unsafe_allow_html=True)
    if not st.session_state.carrello: st.write("Vuoto.")
    else:
        tot = sum(i['p'] for i in st.session_state.carrello)
        for i in st.session_state.carrello: st.write(f"✅ {i['n']} - {i['p']}€")
        st.markdown(f"<h3 style='text-align:right;'>Totale: {tot:.2f}€</h3>", unsafe_allow_html=True)
        if st.button("PAGA ORA"): st.success("Reindirizzamento Stripe...")

elif st.session_state.pagina == "ChiSiamo":
    st.markdown('<div style="text-align:center; padding:20px;"><h2>Chi siamo? ❤️</h2><b>Siamo genitori, come te.</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="obiettivo-pink"><b>Il nostro obiettivo?</b><br>Risparmio e un futuro migliore per i nostri figli.</div>', unsafe_allow_html=True)

