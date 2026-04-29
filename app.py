import streamlit as st
import pandas as pd
import requests
import hashlib
import base64
import os
from datetime import date, datetime, timedelta

# --- 1. CONFIGURAZIONE DATABASE & SICUREZZA ---
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
    # Salva su SheetDB
    requests.post(API_URL, json={"data": [dati]})

def aggiorna_user(email, dati):
    # Aggiorna riga esistente
    requests.patch(f"{API_URL}/email/{email}", json={"data": dati})

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 2. CONFIGURAZIONE PAGINA ---
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
    .header-custom {{ background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); height: 45px; }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    .accent {{ color: #f43f5e; font-weight: 800; text-transform: uppercase; font-size: 12px; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO ---
df_globale = carica_db()

if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; padding:0 30px;'>L'armadio circolare che cresce con il tuo bambino.</p>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")

    elif st.session_state.pagina == "Login":
        st.markdown('<h3 style="text-align:center;">Accedi ✨</h3>', unsafe_allow_html=True)
        with st.form("login"):
            e = st.text_input("Email").strip().lower()
            p = st.text_input("Password", type="password").strip()
            if st.form_submit_button("ENTRA"):
                if not df_globale.empty:
                    hp = hash_password(p)
                    # Supporta sia colonna 'password' che 'pass'
                    p_col = 'password' if 'password' in df_globale.columns else 'pass'
                    user_match = df_globale[(df_globale['email'].str.lower() == e) & (df_globale[p_col] == hp)]
                    if not user_match.empty:
                        st.session_state.user = user_match.iloc[-1].to_dict()
                        vai("Home")
                    else: st.error("Email o Password errati.")
                else: st.error("Nessun utente nel database.")
        if st.button("Non hai un account? Registrati"): vai("Registrazione")

    elif st.session_state.pagina == "Registrazione":
        st.markdown('<h3 style="text-align:center;">Crea Account ✨</h3>', unsafe_allow_html=True)
        with st.form("reg"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            nome = st.text_input("Il tuo Nome")
            bimbo = st.text_input("Nome Bambino")
            taglia = st.selectbox("Taglia Attuale", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            locker = st.selectbox("Locker preferito", ["InPost", "Esselunga", "Poste Italiane"])
            if st.form_submit_button("REGISTRATI ORA"):
                if email and password:
                    nuovo = {
                        "email": email.strip().lower(),
                        "password": hash_password(password),
                        "nome": nome,
                        "bimbo": bimbo,
                        "taglia": taglia,
                        "inizio": str(date.today()),
                        "scadenza": str(date.today() + timedelta(days=90)),
                        "locker": locker
                    }
                    registra_user(nuovo)
                    st.success("Account creato! Fai il login.")
                    vai("Login")
        if st.button("Torna al Login"): vai("Login")

# --- 5. APP DOPO LOGIN ---
else:
    # --- BARRA NAVIGAZIONE FISSA (7 ICONE) ---
    c = st.columns(7)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("🛒", "Carrello"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
    
    st.divider()

    # --- PAGINE ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome_m = st.session_state.user.get('nome', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:28px; font-weight:800;">Ciao {nome_m}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)

    elif st.session_state.pagina == "Info":
        st.markdown("### Guida LoopBaby 🔄")
        st.markdown("""
        <div class="info-box"><span class="accent">🚚 CONSEGNA</span><br>Riceverai la Box entro 3-5 giorni nel Locker InPost scelto.</div>
        <div class="info-box"><span class="accent">🔄 CAMBIO TAGLIA</span><br>Ordina la taglia nuova e rendi la vecchia insieme. Semplice.</div>
        <div class="info-box"><span class="accent">🧼 IGIENE</span><br>Sanificazione professionale certificata per ogni capo.</div>
        """, unsafe_allow_html=True)

    elif st.session_state.pagina == "Profilo":
        st.markdown("### Il tuo Profilo 👤")
        if not st.session_state.edit_mode:
            st.markdown(f"""<div class="card" style="text-align:left;">
                <b>👤 Nome:</b> {st.session_state.user.get('nome')}<br>
                <b>👶 Bambino:</b> {st.session_state.user.get('bimbo')}<br>
                <b>📏 Taglia:</b> {st.session_state.user.get('taglia')}<br>
                <b>📍 Locker:</b> {st.session_state.user.get('locker')}<hr>
                <b>📅 Scadenza:</b> {st.session_state.user.get('scadenza')}
            </div>""", unsafe_allow_html=True)
            if st.button("MODIFICA DATI"): st.session_state.edit_mode = True; st.rerun()
            if st.button("LOGOUT"): st.session_state.user = None; vai("Welcome")
        else:
            with st.form("edit"):
                n = st.text_input("Nome", st.session_state.user.get('nome'))
                nb = st.text_input("Bimbo", st.session_state.user.get('bimbo'))
                if st.form_submit_button("SALVA"):
                    aggiorna_user(st.session_state.user['email'], {"nome": n, "bimbo": nb})
                    st.session_state.edit_mode = False; vai("Profilo")

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("### La nostra missione ❤️")
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">'
                    'Siamo genitori che hanno deciso di dire basta allo spreco. '
                    'Abbiamo creato <b>LoopBaby</b> per far viaggiare la qualità di famiglia in famiglia, '
                    'seguendo la crescita dei piccoli senza sprechi di soldi e spazio. 🌿</div>', unsafe_allow_html=True)
