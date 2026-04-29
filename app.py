import streamlit as st
from supabase import create_client, Client
import base64
import os

# --- 1. CONNESSIONE (FIX 404) ---
# Assicurati che l'URL sia esattamente questo e finisca con .co
URL = "https://supabase.co"
KEY = "sb_publishable_9t_Psdh5tIz9OsfrSAwuMw_hJQ9i89Z"

# Inizializzazione forzata
@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

# --- 2. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}

def vai(p): st.session_state.pagina = p

# --- 3. FUNZIONI ---
def login(e, p):
    try:
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        # Carica dati profilo
        d = supabase.table("profili").select("*").eq("id", res.user.id).execute()
        if d.data: st.session_state.dati = d.data[0]
        vai("Home"); st.rerun()
    except: st.error("Accesso fallito. Hai confermato la mail?")

def registro(e, p):
    try:
        supabase.auth.sign_up({"email": e, "password": p})
        st.success("📩 Mail inviata! Clicca sul link per attivare.")
    except Exception as err: st.error(f"Errore: {err}")

def salva_profilo(d):
    d["id"] = st.session_state.user.id
    supabase.table("profili").upsert(d).execute()
    st.session_state.dati = d
    st.success("✅ Salvato online!")

def get_b64(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

img, logo = get_b64("bimbo.jpg"), get_b64("logo.png")

# --- 4. STILE ---
st.markdown(f"""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #FDFBF7; max-width: 450px; margin: 0 auto; padding-bottom: 100px; }}
    .header {{ background-image: linear-gradient(rgba(0,0,0,0.1),rgba(0,0,0,0.1)), url("data:image/png;base64,{logo}"); background-size: cover; height: 130px; display: flex; align-items: center; justify-content: center; border-radius: 0 0 30px 30px; margin-bottom: 20px; }}
    .header-t {{ color: white; font-size: 30px; font-weight: 800; text-transform: uppercase; }}
    div.stButton > button {{ background: #f43f5e !important; color: white !important; border-radius: 15px; width: 100%; font-weight: 700; border: none; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
    .card {{ border-radius: 20px; padding: 20px; margin: 10px; border: 1px solid #EAE2D6; background: white; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGICA PAGINE ---
if st.session_state.user is None:
    st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA"): vai("Login"); st.rerun()
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"): login(e, p)
        with t2:
            with st.form("r"):
                er, pr = st.text_input("Email "), st.text_input("Password (min 6 car.)", type="password")
                if st.form_submit_button("CREA ACCOUNT"): registro(er, pr)
else:
    if st.session_state.pagina == "Home":
        st.markdown(f'<div class="header"><div class="header-t">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.dati.get('nome_genitore', 'Mamma')
        st.markdown(f"### Ciao {nome}! 👋")
        st.markdown(f'<img src="data:image/jpeg;base64,{img}" style="width:100%; border-radius:20px;">', unsafe_allow_html=True)
        if st.button("Logout"): 
            supabase.auth.sign_out()
            st.session_state.user = None; st.rerun()

    elif st.session_state.pagina == "Profilo":
        st.markdown("## Profilo 👤")
        with st.form("p"):
            n = st.text_input("Nome", st.session_state.dati.get('nome_genitore', ''))
            nb = st.text_input("Bimbo", st.session_state.dati.get('nome_bambino', ''))
            tg = st.selectbox("Taglia", ["50-56 cm", "62-68 cm", "74-80 cm", "86-92 cm"])
            if st.form_submit_button("SALVA NEL DATABASE"): 
                salva_profilo({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("## Chi Siamo ❤️")
        st.markdown('<div class="card">Siamo genitori come te. LoopBaby nasce per ridurre gli sprechi e aiutarti a risparmiare.</div>', unsafe_allow_html=True)

    # BARRA NAVIGAZIONE
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(6)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("🛍️", "Vetrina"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"n_{pag}"): vai(pag); st.rerun()
