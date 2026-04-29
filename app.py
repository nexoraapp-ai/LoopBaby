import streamlit as st
from supabase import create_client, Client
import base64
import os

# --- 1. CONNESSIONE (FIX PROXY ERROR) ---
URL_DB: str = "https://supabase.co"
KEY_DB: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

# Inizializzazione sicura
@st.cache_resource
def get_supabase_client():
    # Rimuoviamo opzioni extra per evitare conflitti di versione
    return create_client(URL_DB, KEY_DB)

try:
    supabase = get_supabase_client()
except Exception as e:
    st.error(f"Errore connessione: {e}")
    st.stop()

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "dati" not in st.session_state: st.session_state.dati = {}

def vai(nome): 
    st.session_state.pagina = nome
    st.rerun()

# --- 3. FUNZIONI ---
def login(e, p):
    try:
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        d = supabase.table("profili").select("*").eq("id", res.user.id).execute()
        if d.data: st.session_state.dati = d.data[0]
        vai("Home")
    except: st.error("Accesso fallito. Mail confermata?")

def registro(e, p):
    try:
        supabase.auth.sign_up({"email": e, "password": p})
        st.success("📩 Conferma la mail (guarda anche in Spam)!")
    except Exception as err: st.error(f"Errore: {err}")

def salva_db(d):
    d["id"] = st.session_state.user.id
    supabase.table("profili").upsert(d).execute()
    st.session_state.dati = d
    st.success("✅ Salvato!")

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

# --- 5. LOGICA ---
if st.session_state.user is None:
    st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.button("ENTRA"): login(e, p)
        with t2:
            er = st.text_input("Email ")
            pr = st.text_input("Scegli Password", type="password")
            if st.button("CREA ACCOUNT"): registro(er, pr)
else:
    if st.session_state.pagina == "Home":
        st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.dati.get('nome_genitore', 'Mamma')
        st.markdown(f"### Ciao {nome}! 👋")
        st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:20px;">', unsafe_allow_html=True)
        if st.button("Logout"): 
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    elif st.session_state.pagina == "Profilo":
        with st.form("p"):
            n = st.text_input("Nome", st.session_state.dati.get('nome_genitore', ''))
            nb = st.text_input("Bimbo", st.session_state.dati.get('nome_bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm"])
            if st.form_submit_button("SALVA SUL DATABASE"): 
                salva_db({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})

    # Barra Nav
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(4)
    menu = [("🏠", "Home"), ("📖", "Info"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
