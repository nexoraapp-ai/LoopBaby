import streamlit as st
from supabase import create_client, Client
import base64
import os

# --- 1. CONNESSIONE SUPABASE ---
URL_PROGETTO = "https://supabase.co"
CHIAVE_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def get_client():
    return create_client(URL_PROGETTO, CHIAVE_ANON)

supabase: Client = get_client()

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "dati" not in st.session_state: st.session_state.dati = {}
if "edit_mode" not in st.session_state: st.session_state.edit_mode = False

def vai(p): 
    st.session_state.pagina = p
    st.rerun()

# --- 3. FUNZIONI LOGICHE ---
def login(e, p):
    try:
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        # Carica dati profilo
        try:
            d = supabase.table("profili").select("*").eq("id", res.user.id).execute()
            if d.data: st.session_state.dati = d.data[0]
        except: pass
        vai("Home")
    except: st.error("Email o Password errati.")

def registrazione(e, p):
    try:
        supabase.auth.sign_up({"email": e, "password": p})
        st.success("📩 Mail inviata! Controlla la posta (e lo Spam).")
    except Exception as err:
        st.error(f"Errore tecnico: {err}")

def salva_profilo(d):
    try:
        d["id"] = st.session_state.user.id
        supabase.table("profili").upsert(d).execute()
        st.session_state.dati = d
        st.success("✅ Salvato!")
    except: st.error("Errore nel salvataggio.")

def get_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img, logo = get_b64("bimbo.jpg"), get_b64("logo.png")

# --- 4. CSS ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7; max-width: 450px; margin: 0 auto; padding-bottom: 100px; }}
    .header {{ background-image: linear-gradient(rgba(0,0,0,0.1),rgba(0,0,0,0.1)), url("data:image/png;base64,{logo}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 20px; }}
    .header-t {{ color: white; font-size: 30px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background: #f43f5e !important; color: white !important; border-radius: 15px; width: 100%; font-weight: 700; border: none; }}
    .card {{ border-radius: 20px; padding: 20px; margin: 10px; border: 1px solid #EAE2D6; background: white; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. PAGINE ---
if st.session_state.user is None:
    st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            e = st.text_input("Email", key="login_email")
            p = st.text_input("Password", type="password", key="login_pass")
            if st.button("ENTRA", key="btn_login"): login(e, p)
        with t2:
            er = st.text_input("La tua migliore Email", key="reg_email")
            pr = st.text_input("Scegli Password", type="password", key="reg_pass")
            if st.button("CREA ACCOUNT", key="btn_reg"): registrazione(er, pr)
else:
    if st.session_state.pagina == "Home":
        st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.dati.get('nome_genitore', 'Mamma')
        st.markdown(f"### Ciao {nome}! 👋")
        if img: st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:20px;">', unsafe_allow_html=True)
        if st.button("Logout"): 
            supabase.auth.sign_out()
            st.session_state.user = None
            vai("Welcome")
    
    elif st.session_state.pagina == "Profilo":
        st.markdown("## Il tuo Profilo 👤")
        with st.form("form_profilo"):
            n = st.text_input("Tuo Nome", st.session_state.dati.get('nome_genitore', ''))
            nb = st.text_input("Nome Bambino", st.session_state.dati.get('nome_bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA ONLINE"):
                salva_profilo({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})

    elif st.session_state.pagina == "Info":
        st.markdown("## Come Funziona 🔄")
        st.write("Dettagli in arrivo...")

    # Barra Navigazione
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📖", "Info"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
