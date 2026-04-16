import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="favicon.ico", layout="centered")

# --- 2. STILE GRAFICO (VERSIONE FIXATA) ---
# Usiamo le doppie graffe {{ }} e carichiamo il CSS in un blocco unico e pulito
st.markdown("""
    <style>
    /* Nasconde header e footer di Streamlit */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Sfondo e Contenitore */
    .stApp { 
        background-color: #f0fdfa !important; 
        max-width: 500px !important; 
        margin: 0 auto !important; 
    }
    
    /* Testi */
    h1, h2, h3, h4, p, span, label { color: #0d9488 !important; font-family: 'sans-serif'; }
    
    /* PULSANTI: Forza il colore e nasconde il codice */
    .stButton>button { 
        border-radius: 30px !important; 
        height: 3.5em !important; 
        font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; 
        border: none !important; 
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
        margin-top: 10px;
    }
    
    .stButton>button:hover { color: white !important; opacity: 0.9; }

    /* CARD */
    .card { 
        background: white; 
        padding: 20px; 
        border-radius: 20px; 
        border: 1px solid #0d9488; 
        margin-bottom: 20px; 
    }
    .promo-card { 
        background: #fef3c7; 
        padding: 20px; 
        border-radius: 20px; 
        border: 2px solid #d97706; 
        text-align: center; 
        margin-bottom: 20px; 
    }
    .price-tag { 
        font-size: 1.2em; 
        font-weight: bold; 
        color: #e11d48 !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma", "bimbo": "Bimbo/a", "cellulare": "", "email": "",
        "ha_ordinato": False, "data_ordine": None, "taglia": "0-1m"
    }

# --- 4. ACCESSO ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("ENTRA"):
            if email == "admin" and password == "baby2024":
                st.session_state.autenticato = "admin"
                st.rerun()
            elif email:
                st.session_state.user_data["email"] = email
                st.session_state.autenticato = "utente"
                st.rerun()
                
    with tab2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Tuo Nome", key="reg_nome")
        c_m = st.text_input("N° Telefono", key="reg_tel")
        n_b = st.text_input("Nome del Bimbo/a", key="reg_bimbo")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0, key="reg_peso")
        if st.button("REGISTRATI ORA"):
            if n_m and c_m:
                tg = "0-1m" if p_b < 4.5 else "1-3m" if p_b < 5.5 else "3-6m" if p_b < 7.5 else "6-9m" if p_b < 9.0 else "12-24m"
                st.session_state.user_data.update({"nome": n_m, "bimbo": n_b, "cellulare": c_m, "taglia": tg})
                st.session_state.autenticato = "utente"
                st.session_state.iscritti += 1
                st.rerun()
    st.stop()

# --- 5. SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    st.write(f"Ciao **{st.session_state.user_data['nome']}**! 🧸")
    scelta = st.radio("Menu:", ["🏠 Home", "📝 Profilo", "📦 Box Loop", "🛍️ Vetrina Shopping", "🔐 Admin"])
    if st.button("Esci"):
        st.session_state.autenticato = False
        st.rerun()

# --- 6. PAGINE ---
if scelta == "🏠 Home":
    st.title("Benvenuta! ✨")
    st.markdown(f"""
        <div class="promo-card">
            <h2>🚀 PROMO FONDATRICI</h2>
            <p>1ª BOX OMAGGIO E RITIRO GRATIS!</p>
            <div style="font-size:1.5em; font-weight:800;">{st.session_state.iscritti} / 50 posti occupati</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
            <h4>Il tuo armadio circolare 🌿</h4>
            <p>Scegli il tuo box, usalo e cambialo quando il bimbo cresce. Risparmia tempo, spazio e denaro.</p>
        </div>
    """, unsafe_allow_html=True)

elif scelta == "📝 Profilo":
    st.title("I tuoi dati 📝")
    with st.form("form_p"):
        u_nome = st.text_input("Nome", st.session_state.user_data["nome"])
        u_tel = st.text_input("Telefono", st.session_state.user_data["cellulare"])
        u_taglia = st.selectbox("Taglia Bimbo", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.form_submit_button("SALVA"):
            st.session_state.user_data.update({"nome": u_nome, "cellulare": u_tel, "taglia": u_taglia})
            st.success("Dati aggiornati!")

elif scelta == "📦 Box Loop":
    st.title("I nostri Box 📦")
    st.markdown('<div class="card"><b>Standard Loop</b><br><span class="price-tag">19,90€</span></div>', unsafe_allow_html=True)
    st.button("ORDINA STANDARD", key="btn_std")
    st.markdown('<div class="card"><b>Premium Loop</b><br><span class="price-tag">29,90€</span></div>', unsafe_allow_html=True)
    st.button("ORDINA PREMIUM", key="btn_pre")

elif scelta == "🛍️ Vetrina Shopping":
    st.title("Vetrina 🛍️")
    st.info("Consegna GRATIS sopra i 50€")
    st.markdown('<div class="card">🌱 <b>Set 3 Body Bio</b><br><span class="price-tag">18,00€</span></div>', unsafe_allow_html=True)
    st.button("ACQUISTA SET", key="buy1")

elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Pannello Admin 🔐")
        st.write("Gestione Mamme Iscritte")
        # Link rapido mail
        st.markdown("[✉️ Invia Email Assistenza](mailto:info@loopbaby.it)")
    else:
        st.error("Non hai i permessi.")
