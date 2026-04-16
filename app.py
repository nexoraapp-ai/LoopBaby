import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO (CSS TOTALE) ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Forza testo scuro per visibilità */
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #0d9488 !important; }
    
    /* Pulsanti */
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    /* Card Strutturate */
    .vision-card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .costi-card { background: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; margin-bottom: 20px; }
    .tracker-box { background: white; padding: 15px; border-radius: 20px; border: 2px solid #0d9488; margin-bottom: 20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "bimbo": "", "cellulare": "", 
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire"
    }

# --- 4. LOGIN / REGISTRAZIONE (CON RICHIESTA TELEFONO) ---
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
        c_m = st.text_input("N° Telefono (per consegne e allert)")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and c_m:
                tg = "0-1m" if p_b < 4.5 else "1-3m" if p_b < 5.5 else "3-6m" if p_b < 7.5 else "6-9m" if p_b < 9.0 else "12-24m"
                st.session_state.user_data.update({"nome": n_m, "bimbo": n_b, "cellulare": c_m, "taglia": tg})
                st.session_state.autenticato = "utente"
                st.session_state.iscritti += 1
                st.rerun()
    st.stop()

# --- 5. MENU ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.write(f"Ciao {st.session_state.user_data['nome']}! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME PAGE ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")

    # Tracker 90 giorni
    if st.session_state.user_data["ha_ordinato"] and st.session_state.user_data["data_ordine"]:
        df = st.session_state.user_data["data_ordine"] + timedelta(days=90)
        gm = (df - datetime.now()).days
        st.markdown(f'<div class="tracker-box">📅 <b>Loop in corso: Giorno {90-gm} di 90</b><br>Mancano {gm} giorni al cambio taglia.</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="vision-card">
        <h4>Cos'è LoopBaby? 🌿</h4>
        <p>L'armadio circolare intelligente. <b>Risparmi oltre 1.000€ l'anno!</b></p>
        <p>Scegli la tua Box (Standard 19,90€ o Premium 29,90€) con trasporto incluso. 
        Usala per 3 mesi e cambiala al cambio taglia. 
        <b>Il Reso:</b> Gratis se rinnovi, oppure 7,90€ se decidi di fermarti.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <p><b>Ritiro Locker GRATIS e 1° BOX OMAGGIO!</b><br>Per le prime 50 mamme che inviano 10+ capi usati.</p>
        <div style="font-size:1.3em; font-weight:bold;">{st.session_state.iscritti} / 50 posti occupati</div>
    </div>
    """, unsafe_allow_html=True)

# --- 7. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    st.write(f"**Mamma:** {st.session_state.user_data['nome']}")
    st.write(f"**Telefono:** {st.session_state.user_data['cellulare']}")
    st.write(f"**Bimbo/a:** {st.session_state.user_data['bimbo']}")
    st.write(f"**Taglia attuale:** {st.session_state.user_data['taglia']}")

# --- 8. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19,90 €)")
    st.write("10 capi igienizzati. Spedizione inclusa!")
    for s in ["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"]:
        with st.expander(f"Vedi dettagli {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s):
            st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
            st.success("Ordine effettuato! Countdown 90 giorni iniziato.")

# --- 9. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29,90 €)")
    st.write("10 capi Grandi Firme (Nike, Adidas, Ralph Lauren).")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    if st.button("ORDINA PREMIUM"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
        st.balloons()

# --- 10. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.info("I capi in vetrina si comprano e non si rendono! Gratis > 50€")
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
        st.button("Compra", key="v1")
    with col2:
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button("Compra", key="v2")

# --- 11. ADMIN ---
elif scelta == "🔐 Admin":
    st.title("Area Gestione 🔐")
    st.write(f"Iscritti: **{st.session_state.iscritti}**")
    cel = st.session_state.user_data["cellulare"]
    if cel:
        msg = urllib.parse.quote(f"Ciao {st.session_state.user_data['nome']}! Sono di LoopBaby...")
        st.markdown(f'<a href="https://wa.me{cel}?text={msg}"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%;">📲 CONTATTA SU WHATSAPP</button></a>', unsafe_allow_html=True)
