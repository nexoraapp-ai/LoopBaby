import streamlit as st
from supabase import create_client
import base64
import os

# =========================
# 🔐 SUPABASE CONNECTION
# =========================
URL_DB = "https://supabase.co"
KEY_DB = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6eWZ6cXlvcG1wdmlqZHRmcWZlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczOTkzMzYsImV4cCI6MjA5Mjk3NTMzNn0.yRrzj1Op5UntjxzXsP1tY7lB3SNn3MICc6d9T0JwDWg"
supabase = create_client(URL_DB, KEY_DB)

# =========================
# ⚙️ STATE & NAV
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "dati" not in st.session_state: st.session_state.dati = {}
if "carrello" not in st.session_state: st.session_state.carrello = []

def vai(p):
    st.session_state.pagina = p
    st.rerun()

# =========================
# 🚀 FUNZIONI CORE (FIX DEFINITIVO)
# =========================

def carica_profilo(user_id):
    try:
        res = supabase.table("profili").select("*").eq("id", user_id).execute()
        if res.data and len(res.data) > 0:
            st.session_state.dati = res.data[0]
        else:
            # Se per qualche motivo il profilo non esiste, lo creiamo ora
            nuovo = {"id": user_id, "nome_genitore": "Mamma/Papà"}
            supabase.table("profili").insert(nuovo).execute()
            st.session_state.dati = nuovo
    except:
        st.session_state.dati = {"nome_genitore": "Mamma/Papà"}

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = res.user
        carica_profilo(res.user.id)
        vai("Home")
    except:
        st.error("Credenziali errate. Riprova.")

def registra(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            st.session_state.user = res.user
            # Crea il profilo iniziale
            nuovo = {"id": res.user.id, "nome_genitore": "Mamma/Papà"}
            supabase.table("profili").upsert(nuovo).execute()
            st.session_state.dati = nuovo
            st.success("Account creato con successo!")
            vai("Home")
    except Exception as e:
        st.error(f"Errore: {e}")

# --- CSS PROFESSIONALE ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #FDFBF7; }
    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 20px !important; width: 100% !important; font-weight: bold !important;
        border: none !important; height: 45px !important;
    }
    .card {
        border-radius: 20px; padding: 20px; background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        border: 1px solid #EAE2D6;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🏠 LOGICA NAVIGAZIONE
# =========================

if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center; color:#1e293b;'>👶 LOOPBABY</h1>", unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<div class='card' style='text-align:center;'><h3>L'armadio circolare che cresce con il tuo bambino 🔄</h3></div>", unsafe_allow_html=True)
        if st.button("INIZIA ORA"): vai("Login")

    elif st.session_state.pagina == "Login":
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("f_login"):
                e = st.text_input("Email", key="le")
                p = st.text_input("Password", type="password", key="lp")
                if st.form_submit_button("ENTRA"): login(e, p)
        with t2:
            with st.form("f_reg"):
                er = st.text_input("Email", key="re")
                pr = st.text_input("Password", type="password", key="rp")
                if st.form_submit_button("CREA ACCOUNT"): registra(er, pr)
else:
    # --- BARRA NAVIGAZIONE FISSA ---
    st.markdown("---")
    cols = st.columns(5)
    with cols[0]: 
        if st.button("🏠"): vai("Home")
    with cols[1]: 
        if st.button("📦"): vai("Box")
    with cols[2]: 
        if st.button("👤"): vai("Profilo")
    with cols[3]: 
        if st.button("👋"): vai("ChiSiamo")
    with cols[4]:
        if st.button("🚪"): 
            supabase.auth.sign_out()
            st.session_state.user = None
            vai("Welcome")

    # ---------------- PAGINE ----------------
    if st.session_state.pagina == "Home":
        nome = st.session_state.dati.get("nome_genitore", "Mamma")
        st.markdown(f"<h2>Ciao {nome}! 👋</h2>", unsafe_allow_html=True)
        st.markdown("<div class='card'>✨ <b>Promo Fondatrici</b><br>Dona 10 capi e ricevi una Box OMAGGIO.</div>", unsafe_allow_html=True)

    elif st.session_state.pagina == "Profilo":
        st.title("Tuo Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.dati.get("nome_genitore",""))
            nb = st.text_input("Nome Bambino", st.session_state.dati.get("nome_bambino",""))
            tg = st.selectbox("Taglia", ["50-56","62-68","74-80"], index=0)
            if st.form_submit_button("SALVA DATI"):
                supabase.table("profili").upsert({"id": st.session_state.user.id, "nome_genitore": n, "nome_bambino": nb, "taglia": tg}).execute()
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": nb, "taglia": tg})
                st.success("Dati aggiornati!")

    elif st.session_state.pagina == "Box":
        st.title("Scegli la tua Box 📦")
        st.markdown("<div class='card'><b>Box LUNA 🌙</b><br>19,90€</div>", unsafe_allow_html=True)
        if st.button("Aggiungi al carrello"): st.toast("Aggiunta!")

    elif st.session_state.pagina == "ChiSiamo":
        st.title("Chi Siamo ❤️")
        st.markdown("<div class='card'>Siamo genitori come te. LoopBaby nasce per ridurre gli sprechi e far risparmiare le famiglie offrendo capi di qualità.</div>", unsafe_allow_html=True)
