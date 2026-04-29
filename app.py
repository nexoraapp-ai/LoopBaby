import streamlit as st
from supabase import create_client, Client
import base64
import os
from datetime import datetime, timedelta

# --- 1. CONNESSIONE SUPABASE ---
URL_DB = "https://supabase.co"
KEY_DB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def init_connection():
    return create_client(URL_DB, KEY_DB)

supabase = init_connection()

# --- 2. CONFIGURAZIONE E STATO ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}

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
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{ background-color: #f43f5e !important; color: white !important; border-radius: 18px !important; width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.2); }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .avviso-scadenza {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 20px; border: 1px solid #f87171; font-weight: 800; text-align: center; margin: 15px; font-size: 13px; }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCOUNT ---
def login(e, p):
    try:
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        # Carica dati dal database
        d = supabase.table("profili").select("*").eq("id", res.user.id).execute()
        if d.data: st.session_state.dati = d.data[0]
        vai("Home")
    except: st.error("Accesso fallito. Controlla email e password.")

def registrazione(e, p):
    try:
        supabase.auth.sign_up({"email": e, "password": p})
        st.success("📩 Mail inviata! Conferma l'account per entrare.")
    except Exception as err: st.error(f"Errore: {err}")

def salva_profilo(dati_nuovi):
    try:
        dati_nuovi["id"] = st.session_state.user.id
        supabase.table("profili").upsert(dati_nuovi).execute()
        st.session_state.dati = dati_nuovi
        st.success("✅ Salvato online su Supabase!")
    except Exception as e: st.error(f"Errore salvataggio: {e}")

# --- 5. PAGINE ---
if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            e = st.text_input("Email", key="l_e")
            p = st.text_input("Password", type="password", key="l_p")
            if st.button("ENTRA"): login(e, p)
        with t2:
            er = st.text_input("La tua migliore Email", key="r_e")
            pr = st.text_input("Scegli Password (min 6 car.)", type="password", key="r_p")
            if st.button("CREA ACCOUNT"): registrazione(er, pr)
else:
    # AVVISO SCADENZA (Calcolo automatico se esiste data nel DB)
    scad = st.session_state.dati.get('scadenza')
    if scad:
        giorni = (datetime.strptime(scad, "%Y-%m-%d") - datetime.now()).days
        if 0 <= giorni <= 10:
            st.markdown(f'<div class="avviso-scadenza">⚠️ Mancano {giorni} giorni al cambio Box!</div>', unsafe_allow_html=True)

    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.dati.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;"><div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio circolare.</div></div><div>{img_h}</div></div>""", unsafe_allow_html=True)
        if st.button("Logout"): 
            supabase.auth.sign_out()
            st.session_state.user = None; vai("Welcome")

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.dati.get('nome_genitore', ''))
            nb = st.text_input("Nome Bambino", st.session_state.dati.get('nome_bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA NEL DATABASE"):
                salva_profilo({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("## Chi Siamo ❤️")
        st.markdown('<div class="card">Siamo genitori come te. LoopBaby nasce per eliminare lo spreco e farti risparmiare più di 1000€ l\'anno.</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    m_list = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Shop"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(m_list):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
