import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- STILE GRAFICO PULITO (MOBILE OPTIMIZED) ---
st.markdown("""
    <style>
    /* Nasconde header e footer Streamlit */
    header, footer, #MainMenu {visibility: hidden;}
    
    .stApp { background-color: #f0fdfa; }
    
    /* Pulsanti Moderni */
    .stButton>button { 
        border-radius: 25px; height: 3.5em; font-weight: bold; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); 
        color: white; border: none; width: 100%; 
    }
    
    /* Box Passaggi */
    .step-box { 
        background-color: #ffffff; padding: 20px; border-radius: 20px; 
        border: 2px solid #0d9488; text-align: center; margin-bottom: 15px; 
    }
    .step-box h3 { color: #0d9488; font-size: 1.1em; font-weight: 900; }
    
    /* Card Risparmio */
    .savings-card { 
        background-color: #d1fae5; padding: 15px; border-radius: 20px; 
        border: 2px dashed #059669; text-align: center; margin-bottom: 20px; 
        color: #065f46; font-weight: bold;
    }
    
    /* Card Promozioni */
    .promo-card { 
        background-color: #e0f2fe; padding: 20px; border-radius: 20px; 
        border-left: 10px solid #0369a1; margin-bottom: 20px; color: #0c4a6e; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIONE LOGIN ---
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>L'armadio sostenibile 0-24 mesi</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    with tab1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"
            elif e and p: st.session_state.autenticato = "utente"
            st.rerun()
    with tab2:
        st.write("### Diventa Mamma Fondatrice")
        st.write("Iscriviti ora: Ritiro Gratis + 1° Box Omaggio!")
        st.button("REGISTRATI ORA")
    st.stop()

# --- MENU LATERALE ---
with st.sidebar:
    st.title("🧸 LoopBaby")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin":
        menu.append("🔐 Area Admin")
    scelta = st.sidebar.radio("Naviga:", menu)
    if st.button("Esci"):
        st.session_state.autenticato = False
        st.rerun()

# --- SEZIONI ---
if scelta == "🏠 Home":
    st.title("🌿 Benvenuti")
    st.markdown('<div class="savings-card">💰 Risparmio Annuale: ~1.048 €</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3></div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3></div>', unsafe_allow_html=True)
    with col_c: st.markdown('<div class="step-box"><h3>🔄 Scambia</h3></div>', unsafe_allow_html=True)

    st.markdown('<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Locker GRATIS e PRIMA BOX OMAGGIO!</div>', unsafe_allow_html=True)

elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard")
    if os.path.exists("vestiti.jpg"):
        st.image("vestiti.jpg", caption="Esempio capi reali")
    st.button("ORDINA A 19€")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium")
    if os.path.exists("scarpe.jpg"):
        st.image("scarpe.jpg", caption="Capi Firmati Selezionati")
    st.button("ORDINA A 29€")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
