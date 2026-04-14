import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- STILE FISSO PER CELLULARE ---
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa !important; }
    
    /* Forza i colori dei pulsanti */
    .stButton>button { 
        background-color: #0d9488 !important;
        color: white !important;
        border-radius: 20px !important;
        height: 3em !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Box bianchi evidenti */
    .step-box { 
        background-color: white !important; 
        padding: 15px; 
        border-radius: 15px; 
        border: 2px solid #0d9488; 
        text-align: center; 
        margin-bottom: 10px;
    }
    
    /* Card Promo Gialla */
    .promo-card { 
        background-color: #fef3c7 !important; 
        padding: 15px; 
        border-radius: 15px; 
        border: 2px solid #d97706; 
        color: #92400e; 
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DI NAVIGAZIONE ---
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire"}

# --- LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align:center; color:#0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    with tab1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            st.session_state.autenticato = "utente"
            st.rerun()
    with tab2:
        nm = st.text_input("Il tuo Nome")
        if st.button("REGISTRATI"):
            st.session_state.user_data["nome"] = nm
            st.session_state.autenticato = "utente"
            st.rerun()
    st.stop()

# --- MENU LATERALE ---
with st.sidebar:
    st.title("🧸 LoopBaby")
    st.write(f"Ciao **{st.session_state.user_data['nome']}**")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina"])
    if st.button("Esci"):
        st.session_state.autenticato = False
        st.rerun()

# --- PAGINE ---
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown('<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Gratis + 1° Box Omaggio!</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>10 o più pezzi al Locker</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>Capi igienizzati e stirati</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Cambio taglia entro 3 mesi</p></div>', unsafe_allow_html=True)

elif scelta == "📝 Profilo":
    st.title("📝 Il tuo Profilo")
    st.write(f"Nome Mamma: {st.session_state.user_data['nome']}")

elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19€)")
    with st.expander("🔍 Vedi LUNA"):
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
    st.button("Ordina Luna")

elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29€)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("Ordina Premium")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina")
    st.write("Capi da tenere per sempre")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
