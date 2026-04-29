import streamlit as st
from supabase import create_client
import base64
import os

# =========================
# 🔐 SUPABASE CONNECTION
# =========================
URL_DB = st.secrets["SUPABASE_URL"]
KEY_DB = st.secrets["SUPABASE_KEY"]
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
# 🚀 FUNZIONI CORE (FIX LOGIN/REG)
# =========================

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = res.user
        # Carica dati profilo
        prof = supabase.table("profili").select("*").eq("id", res.user.id).execute()
        st.session_state.dati = prof.data[0] if prof.data else {}
        vai("home")
    except:
        st.error("Email o password errati.")

def registra(email, password):
    try:
        # 1. Crea l'utente
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            st.session_state.user = res.user
            # 2. Crea subito una riga vuota nel database profili per evitare l'errore al login
            supabase.table("profili").insert({
                "id": res.user.id, 
                "nome_genitore": "Mamma/Papà", 
                "taglia": "Da scegliere"
            }).execute()
            st.session_state.dati = {"nome_genitore": "Mamma/Papà"}
            vai("home")
    except Exception as e:
        st.error(f"Errore: {e}")

# =========================
# 🎨 INTERFACCIA
# =========================
st.markdown("<h1 style='text-align:center;'>👶 LOOPBABY</h1>", unsafe_allow_html=True)

if st.session_state.user is None:
    if st.session_state.pagina == "Welcome":
        st.write("L'armadio circolare che cresce con il tuo bambino.")
        if st.button("INIZIA"): vai("login")
    
    elif st.session_state.pagina == "login":
        t1, t2 = st.tabs(["Accedi", "Registrati"])
        with t1:
            with st.form("f_login"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ENTRA"): login(e, p)
        with t2:
            with st.form("f_reg"):
                er = st.text_input("Email ")
                pr = st.text_input("Scegli Password")
                if st.form_submit_button("CREA ACCOUNT"): registra(er, pr)

else:
    # BARRA NAVIGAZIONE
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("🏠"): vai("home")
    with c2: 
        if st.button("📦"): vai("box")
    with c3: 
        if st.button("👤"): vai("profilo")
    with c4:
        if st.button("Logout"): 
            supabase.auth.sign_out()
            st.session_state.user = None
            vai("Welcome")

    if st.session_state.pagina == "home":
        nome = st.session_state.dati.get("nome_genitore", "Mamma")
        st.title(f"Ciao {nome}! 👋")
        st.info("Benvenuta nel tuo armadio infinito.")

    elif st.session_state.pagina == "profilo":
        st.title("Tuo Profilo 👤")
        with st.form("p"):
            n = st.text_input("Tuo Nome", st.session_state.dati.get("nome_genitore",""))
            b = st.text_input("Nome Bambino", st.session_state.dati.get("nome_bambino",""))
            if st.form_submit_button("SALVA"):
                supabase.table("profili").upsert({"id": st.session_state.user.id, "nome_genitore": n, "nome_bambino": b}).execute()
                st.session_state.dati.update({"nome_genitore": n, "nome_bambino": b})
                st.success("Dati salvati!")

    elif st.session_state.pagina == "box":
        st.title("Scegli la tua Box 📦")
        st.write("Box Luna 🌙 - 19,90€")
        if st.button("Aggiungi Luna"): st.toast("Aggiunta!")
