import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="logo.png", 
    layout="centered"
)

# --- 2. STILE GRAFICO BLOCCATO (FIX SCRITTE BIANCHE) ---
st.markdown("""
    <style>
    /* Forza il colore di TUTTI i testi a scurire */
    html, body, [data-testid="stAppViewContainer"], .st-emotion-cache-10trblm {
        color: #333333 !important;
    }
    
    /* Forza i titoli (H1, H2, H3) a essere verde scuro o nero */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #0d9488 !important; /* Verde scuro professionale */
    }

    header {visibility: visible !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    .stApp { 
        background-color: #f0fdfa !important; 
        max-width: 500px; 
        margin: 0 auto; 
    }
    
    /* Pulsanti con scritte BIANCHE ben visibili */
    .stButton>button { 
        border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important; 
    }
    
    /* Sidebar: scritte nere per il menu */
    [data-testid="stSidebar"] span {
        color: #333333 !important;
        font-weight: 600;
    }

    .alert-push { 
        background-color: #fff1f2 !important; border: 2px solid #e11d48; 
        padding: 20px; border-radius: 20px; color: #e11d48 !important; text-align: center; 
        font-weight: 800; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATI E SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma Prova", "cellulare": "391234567890", 
        "taglia": "da definire",
        "data_ordine": datetime.now() - timedelta(days=83) 
    }

# --- 4. LOGIN ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            else: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        nm = st.text_input("Nome")
        if st.button("REGISTRATI ORA"):
            st.session_state.user_data["nome"] = nm
            st.session_state.autenticato = "utente"; st.rerun()
    st.stop()

# --- 5. MENU LATERALE ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.markdown(f"### Ciao **{st.session_state.user_data['nome']}**!")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME ---
if scelta == "🏠 Home":
    scadenza = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    giorni_rimasti = (scadenza - datetime.now()).days
    
    if 0 <= giorni_rimasti <= 7:
        st.markdown(f'<div class="alert-push">🔔 NOTIFICA: Mancano {giorni_rimasti} gg alla fine del Loop. Cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    st.title("Benvenuta! 🧸")
    st.write("L'armadio circolare intelligente che cresce con il tuo bambino.")

# --- 7. PROFILO ---
elif scelta == "📝 Profilo Bimbo":
    st.title("Il tuo Profilo 📝")
    st.subheader(f"Mamma: {st.session_state.user_data['nome']}")
    st.write(f"Taglia attuale: **{st.session_state.user_data['taglia']}**")

# --- 8. ADMIN CON WHATSAPP ---
elif scelta == "🔐 Admin":
    st.title("Area Gestione 🔐")
    nome = st.session_state.user_data["nome"]
    tel = st.session_state.user_data["cellulare"]
    msg = urllib.parse.quote(f"Ciao {nome}! 😊 Sono di LoopBaby. Ho visto che mancano pochi giorni alla fine del Loop...")
    st.markdown(f'<a href="https://wa.me{tel}?text={msg}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 15px; border-radius: 10px; font-weight: bold; width: 100%;">📲 CONTATTA SU WHATSAPP</button></a>', unsafe_allow_html=True)

# (Le altre sezioni Box e Vetrina rimangono uguali)
