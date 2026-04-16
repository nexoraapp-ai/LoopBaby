import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE LOGO E TITOLO PC ---
# Questo cambia la scritta "Streamlit" nella scheda del browser sul PC
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="logo.png" if os.path.exists("logo.png") else "🧸", 
    layout="centered"
)

# --- 2. CSS PER NASCONDERE STREAMLIT E FISSARE L'ICONA ---
st.markdown("""
    <style>
    /* Nasconde la corona rossa e il menu tecnico in alto a destra */
    header {visibility: hidden !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Centratura stile App Mobile */
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Stile pulsanti */
    .stButton>button { border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important; color: white !important; border: none !important; width: 100% !important; }
    
    /* Card e Box Home */
    .step-box { background-color: white !important; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; }
    .promo-card { background-color: #fef3c7 !important; padding: 25px; border-radius: 20px; border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "Il mio bimbo", "taglia": "da definire", "data_ordine": datetime.now()}

# --- 4. LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        nm = st.text_input("Nome")
        if st.button("REGISTRATI"):
            if nm: st.session_state.user_data["nome"] = nm; st.session_state.autenticato = "utente"; st.rerun()
    st.stop()

# --- 5. MENU LATERALE ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.write(f"### Ciao **{st.session_state.user_data['nome']}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina"])
    st.write("---")
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. SEZIONI ---
if scelta == "🏠 Home":
    st.markdown("### Benvenuta nel Loop! ✨")
    # Qui inseriremo di nuovo i tuoi box e promozioni...
    st.markdown('<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro Locker GRATIS e 1° BOX OMAGGIO</p></div>', unsafe_allow_html=True)

elif scelta == "📝 Profilo Bimbo":
    st.title("📝 Profilo Bimbo")
    st.write(f"**Bimbo:** {st.session_state.user_data['bimbo']}")
    st.write(f"**Taglia:** {st.session_state.user_data['taglia']}")
    st.info("I dati appariranno qui dopo il primo ordine!")

elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19€)")
    if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg", caption="Esempio Box Standard")
    st.button("Ordina ora")

elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29€)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg", caption="Selezione Grandi Firme")
    st.button("Scegli Premium")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina"); st.success("Pezzi unici da tenere per sempre.")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
