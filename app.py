import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE & FIX ICONA ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# Forzatura Icona per Mobile (Fix cache)
st.markdown("""
    <head>
        <link rel="icon" href="https://githubusercontent.com" type="image/x-icon">
        <link rel="apple-touch-icon" href="https://githubusercontent.com">
    </head>
    """, unsafe_allow_html=True)

# --- 2. STILE GRAFICO ---
st.markdown("""
    <style>
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, p, span, label { color: #0d9488 !important; }
    
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    .card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 15px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; }
    .price-tag { font-size: 1.5rem; font-weight: bold; color: #e11d48 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma", "bimbo": "Bimbo/a", "cellulare": "3330000000", "email": "mamma@esempio.it",
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire"
    }

# --- 4. LOGICA DI ACCESSO ---
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
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Tuo Nome")
        c_m = st.text_input("N° Telefono")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        if st.button("REGISTRATI E BLOCCA PROMO"):
            tg = "0-1m" if p_b < 4.5 else "1-3m" if p_b < 5.5 else "3-6m" if p_b < 7.5 else "6-9m" if p_b < 9.0 else "12-24m"
            st.session_state.user_data.update({"nome": n_m, "bimbo": n_b, "cellulare": c_m, "taglia": tg})
            st.session_state.autenticato = "utente"
            st.session_state.iscritti += 1
            st.rerun()
    st.stop()

# --- 5. MENU ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME ---
if scelta == "🏠 Home":
    st.title(f"Ciao {st.session_state.user_data['nome']}! ✨")
    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <p>1° BOX OMAGGIO E RITIRO GRATIS!<br>Inviaci 10 capi usati del tuo bimbo.</p>
        <div style="font-size:1.3em; font-weight:bold;">{st.session_state.iscritti} / 50 posti occupati</div>
    </div>
    """, unsafe_allow_html=True)

# --- 7. PROFILO (Modificabile) ---
elif scelta == "📝 Profilo":
    st.title("I tuoi Dati 📝")
    with st.form("profilo_form"):
        new_nome = st.text_input("Nome", st.session_state.user_data["nome"])
        new_cell = st.text_input("Telefono", st.session_state.user_data["cellulare"])
        new_bimbo = st.text_input("Nome Bimbo/a", st.session_state.user_data["bimbo"])
        new_taglia = st.selectbox("Taglia Attuale", ["0-1m", "1-3m", "3-6m", "6-9m", "9-12m", "12-18m", "18-24m"], 
                                 index=["0-1m", "1-3m", "3-6m", "6-9m", "9-12m", "12-18m", "18-24m"].index(st.session_state.user_data["taglia"]))
        
        if st.form_submit_state := st.form_submit_button("CONFERMA E SALVA"):
            st.session_state.user_data.update({"nome": new_nome, "cellulare": new_cell, "bimbo": new_bimbo, "taglia": new_taglia})
            st.success("Profilo aggiornato con successo!")

# --- 8. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("Vetrina LoopBaby 🛍️")
    st.info("🚚 Spedizione GRATIS per ordini superiori a 50€!")
    
    prodotti = [
        {"nome": "Set 3 Body Bio", "prezzo": 15.00, "img": "🌱"},
        {"nome": "Sacco Nanna Invernale", "prezzo": 39.00, "img": "😴"},
        {"nome": "Kit Pappa Silicone", "prezzo": 25.00, "img": "🥣"}
    ]
    
    carrello = 0
    for p in prodotti:
        with st.container():
            col1, col2 = st.columns([2, 1])
            col1.markdown(f"**{p['img']} {p['nome']}**")
            col1.markdown(f'<p class="price-tag">{p["prezzo"]}€</p>', unsafe_allow_html=True)
            if col2.button(f"Compra", key=p['nome']):
                st.toast(f"{p['nome']} aggiunto (simulazione)")

# --- 9. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato != "admin":
        st.error("Area riservata!")
    else:
        st.title("Pannello Controllo 🔐")
        # Esempio tabella utenti
        utenti = pd.DataFrame([
            {"Mamma": "Chiara", "Scadenza": "In scadenza", "Tel": "3331234567", "Mail": "chiara@email.it"},
            {"Mamma": "Elena", "Scadenza": "30 giorni", "Tel": "3479876543", "Mail": "elena@email.it"}
        ])
        st.table(utenti)
        
        for i, row in utenti.iterrows():
            st.write(f"**Contatta {row['Mamma']}:**")
            col1, col2 = st.columns(2)
            # WhatsApp
            msg = urllib.parse.quote(f"Ciao {row['Mamma']}, il tuo Loop sta per scadere!")
            col1.markdown(f'[![WhatsApp](https://shields.io)](https://wa.me{row["Tel"]}?text={msg})')
            # Email
            subj = urllib.parse.quote("Aggiornamento da LoopBaby")
            col2.markdown(f'[![Email](https://shields.io)](mailto:{row["Mail"]}?subject={subj})')

