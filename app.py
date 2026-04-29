import streamlit as st
from supabase import create_client
import base64
import os

# =========================
# 🔐 SUPABASE CONNECTION
# =========================
# Nota: Questi funzioneranno solo se li configuri su Streamlit Cloud (vedi punto sotto)
URL_DB = st.secrets["SUPABASE_URL"]
KEY_DB = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL_DB, KEY_DB)

# =========================
# ⚙️ CONFIG & STATE
# =========================
st.set_page_config(page_title="LoopBaby", layout="centered")

if "user" not in st.session_state: st.session_state.user = None
if "pagina" not in st.session_state: st.session_state.pagina = "Welcome"
if "carrello" not in st.session_state: st.session_state.carrello = []
if "dati" not in st.session_state: st.session_state.dati = {}

def vai(p):
    st.session_state.pagina = p
    st.rerun()

def aggiungi(nome, prezzo):
    st.session_state.carrello.append({"nome": nome, "prezzo": prezzo})
    st.toast(f"✅ {nome} aggiunto!")

# --- CSS PER STILE PROFESSIONALE ---
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #FDFBF7; }
    div.stButton > button {
        background-color: #f43f5e !important; color: white !important;
        border-radius: 20px !important; width: 100% !important; font-weight: bold !important;
    }
    .card {
        border-radius: 20px; padding: 20px; background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 🏠 NAVIGATION LOGIC
# =========================

if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center;'>👶 LOOPBABY</h1>", unsafe_allow_html=True)
    
    if st.session_state.pagina == "Welcome":
        st.markdown("<div class='card' style='text-align:center;'><h3>L'armadio circolare che cresce con il tuo bambino 🔄</h3></div>", unsafe_allow_html=True)
        if st.button("INIZIA"): vai("login")

    elif st.session_state.pagina == "login":
        tab1, tab2 = st.tabs(["Accedi", "Registrati"])
        with tab1:
            with st.form("login_form"):
                e = st.text_input("Email")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("ACCEDI"):
                    try:
                        res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                        st.session_state.user = res.user
                        prof = supabase.table("profili").select("*").eq("id", res.user.id).execute()
                        if prof.data: st.session_state.dati = prof.data[0]
                        vai("home")
                    except: st.error("Dati errati")
        with tab2:
            with st.form("reg_form"):
                er = st.text_input("Email")
                pr = st.text_input("Password", type="password")
                if st.form_submit_button("CREA ACCOUNT"):
                    try:
                        supabase.auth.sign_up({"email": er, "password": pr})
                        st.success("📩 Controlla la mail per confermare!")
                    except Exception as err: st.error(str(err))

else:
    # --- BARRA DI NAVIGAZIONE SUPERIORE ---
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("🏠"): vai("home")
    with c2: 
        if st.button("📦"): vai("box")
    with c3: 
        if st.button("👤"): vai("profilo")
    with c4: 
        if st.button("🛒"): vai("carrello")

    # ---------------- HOME ----------------
    if st.session_state.pagina == "home":
        nome = st.session_state.dati.get("nome_genitore", "Mamma")
        st.title(f"Ciao {nome}! 👋")
        
        st.markdown("""
        <div class='card'>
            <b>✨ Promo Mamme Fondatrici</b><br>
            Dona 10 capi e ricevi una Box OMAGGIO!
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Chi Siamo ❤️"): vai("chisiamo")

    # ---------------- BOX ----------------
    elif st.session_state.pagina == "box":
        st.title("Scegli la tua Box 📦")
        col1, col2 = st.columns(2)
        
        boxes = [("Luna 🌙", 19.90, col1), ("Sole ☀️", 19.90, col2), ("Premium 💎", 29.90, st)]
        for n, p, col in boxes:
            with col:
                st.markdown(f"<div class='card'><h3>{n}</h3><p>{p}€</p></div>", unsafe_allow_html=True)
                if st.button(f"Scegli {n}"): aggiungi(n, p)

    # ---------------- PROFILO ----------------
    elif st.session_state.pagina == "profilo":
        st.title("Profilo 👤")
        d = st.session_state.dati
        with st.form("profile"):
            n = st.text_input("Nome genitore", d.get("nome_genitore",""))
            b = st.text_input("Nome bambino", d.get("nome_bambino",""))
            t = st.selectbox("Taglia", ["50-56","62-68","74-80"], index=0)
            if st.form_submit_button("Salva"):
                nuovi_dati = {"id": st.session_state.user.id, "nome_genitore": n, "nome_bambino": b, "taglia": t}
                supabase.table("profili").upsert(nuovi_dati).execute()
                st.session_state.dati = nuovi_dati
                st.success("Dati aggiornati!")

    # ---------------- CARRELLO ----------------
    elif st.session_state.pagina == "carrello":
        st.title("Il tuo ordine 🛒")
        totale = 0
        for i in st.session_state.carrello:
            st.write(f"✅ {i['nome']} - {i['prezzo']}€")
            totale += i['prezzo']
        st.subheader(f"Totale: {totale:.2f}€")
        if totale > 0:
            if st.button("PAGA ORA"): st.info("Reindirizzamento a Stripe...")

    # ---------------- CHI SIAMO ----------------
    elif st.session_state.pagina == "chisiamo":
        st.title("Chi Siamo ❤️")
        st.write("Siamo genitori che credono in un futuro senza sprechi.")
        if st.button("Torna alla Home"): vai("home")
