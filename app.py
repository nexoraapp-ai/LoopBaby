import streamlit as st
from supabase import create_client, Client
import base64
import os
from datetime import datetime

# --- 1. CONNESSIONE SUPABASE (FIX 404 & CHIAVI) ---
URL_DB = "https://supabase.co"
KEY_DB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"

@st.cache_resource
def get_supabase():
    return create_client(URL_DB, KEY_DB)

supabase = get_supabase()

# --- 2. SETUP APP & STATO ---
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
    .header-custom {{
        background-image: linear-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.1)), url("data:image/png;base64,{logo_bg}");
        background-size: cover; background-position: center; height: 130px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 35px; border-radius: 0 0 30px 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .header-text {{ color: white; font-size: 32px; font-weight: 800; letter-spacing: 3px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); text-transform: uppercase; }}
    div.stButton > button {{
        background-color: #f43f5e !important; color: white !important; border-radius: 18px !important;
        width: 100% !important; font-weight: 800 !important; margin: 10px auto !important; border: none !important;
    }}
    .card {{ border-radius: 25px; padding: 20px; margin: 10px 20px; border: 1px solid #EAE2D6; text-align: center; background-color: #FFFFFF; box-shadow: 0 8px 25px rgba(0,0,0,0.03); }}
    .prezzo-rosa {{ color: #ec4899; font-size: 24px; font-weight: 900; }}
    .info-box {{ text-align: left; font-size: 14px; color: #475569; line-height: 1.5; padding: 15px; background: #f8fafc; border-radius: 15px; margin-bottom: 12px; border-left: 5px solid #f43f5e; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGICA ACCESSO ---
def login_user(e, p):
    try:
        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
        st.session_state.user = res.user
        prof = supabase.table("profili").select("*").eq("id", res.user.id).execute()
        st.session_state.dati = prof.data[0] if prof.data else {}
        vai("Home")
    except: st.error("Dati errati")

def registra_user(e, p):
    try:
        res = supabase.auth.sign_up({"email": e, "password": p})
        if res.user:
            supabase.table("profili").upsert({"id": res.user.id, "nome_genitore": "Mamma"}).execute()
            st.success("Registrazione completata! Ora fai il login.")
    except Exception as err: st.error(f"Errore: {err}")

# --- 5. NAVIGAZIONE ---
if st.session_state.user is None:
    st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
    if st.session_state.pagina == "Welcome":
        st.markdown("<h2 style='text-align:center;'>Benvenuta in Famiglia! 🌸</h2>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")
    else:
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("l"):
                e, p = st.text_input("Email"), st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"): login_user(e, p)
        with t2:
            with st.form("r"):
                er, pr = st.text_input("Email "), st.text_input("Password", type="password")
                if st.form_submit_button("CREA ACCOUNT"): registra_user(er, pr)
else:
    # --- APP DOPO LOGIN ---
    if st.session_state.pagina == "Home":
        st.markdown('<div class="header-custom"><div class="header-text">LOOPBABY</div></div>', unsafe_allow_html=True)
        nome = st.session_state.dati.get('nome_genitore', 'Mamma')
        img_h = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:25px;">' if img_data else ""
        st.markdown(f"""<div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 15px; padding: 0 20px;">
            <div><div style="font-size:28px; font-weight:800;">Ciao {nome}! 👋</div><div style="font-size:14px; color:#334155;">Il tuo armadio circolare è pronto.</div></div>
            <div>{img_h}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="card" style="background:#FFF1F2; border:2px dashed #F43F5E;"><b>✨ Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO!</div>', unsafe_allow_html=True)
        if st.button("Scopri di più"): vai("ChiSiamo")

    elif st.session_state.pagina == "ChiSiamo":
        st.markdown("<h2 style='text-align:center;'>La nostra missione ❤️</h2>", unsafe_allow_html=True)
        st.markdown('<div class="card" style="text-align:left; line-height:1.6;">'
                    'Siamo genitori stanchi di vedere sacchi di vestiti ammassati in soffitta. '
                    'Abbiamo creato <b>LoopBaby</b> per far viaggiare i vestiti di famiglia in famiglia, '
                    'seguendo la crescita dei piccoli senza sprechi di soldi e spazio.</div>', unsafe_allow_html=True)
        if st.button("Torna alla Home"): vai("Home")

    elif st.session_state.pagina == "Info":
        st.markdown("<h2 style='text-align:center;'>Guida LoopBaby 🔄</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box"><b>🚚 CONSEGNA:</b> 3-5 giorni lavorativi tramite InPost.</div>
        <div class="info-box"><b>🔄 CAMBIO:</b> Quando i vestiti stringono, ordina la taglia nuova e rendi la vecchia.</div>
        <div class="info-box"><b>🧼 IGIENE:</b> Sanificazione professionale certificata per ogni capo.</div>
        """, unsafe_allow_html=True)

    elif st.session_state.pagina == "Box":
        st.markdown("<h2 style='text-align:center;'>Le tue Box 📦</h2>", unsafe_allow_html=True)
        for s, p in [("LUNA 🌙", 19.90), ("SOLE ☀️", 19.90)]:
            st.markdown(f'<div class="card"><h3>{s}</h3><div class="prezzo-rosa">{p}€</div></div>', unsafe_allow_html=True)
            if st.button(f"Scegli {s}", key=s): st.toast("Aggiunta!")

    elif st.session_state.pagina == "Profilo":
        st.markdown("<h2 style='text-align:center;'>Profilo 👤</h2>", unsafe_allow_html=True)
        st.write(f"Email: {st.session_state.user.email}")
        if st.button("Logout"): 
            supabase.auth.sign_out()
            st.session_state.user = None; vai("Welcome")

    # BARRA NAVIGAZIONE
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    c = st.columns(5)
    menu = [("🏠", "Home"), ("📖", "Info"), ("📦", "Box"), ("👤", "Profilo"), ("👋", "ChiSiamo")]
    for i, (icon, pag) in enumerate(menu):
        with c[i]:
            if st.button(icon, key=f"nav_{pag}"): vai(pag)
