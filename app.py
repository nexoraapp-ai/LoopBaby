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
    
    /* Forza testo scuro */
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #0d9488 !important; }
    
    /* Pulsanti Moderni */
    .stButton>button { 
        border-radius: 30px !important; height: 3.8em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    /* Tracker Loop Style */
    .tracker-box { 
        background: white; padding: 15px; border-radius: 20px; 
        border: 2px solid #0d9488; margin-bottom: 20px; text-align: center;
    }
    
    .alert-scadenza { 
        background-color: #fff1f2 !important; border: 2px solid #e11d48; 
        padding: 20px; border-radius: 20px; color: #e11d48 !important; 
        text-align: center; font-weight: 800; margin-bottom: 25px;
    }
    
    .vision-card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma", "bimbo": "", "ha_ordinato": False, "data_ordine": None, "cellulare": ""
    }

# --- 4. LOGIN / REGISTRAZIONE ---
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
        nm = st.text_input("Il tuo Nome")
        cl = st.text_input("Cellulare")
        if st.button("REGISTRATI"):
            if nm: st.session_state.user_data.update({"nome": nm, "cellulare": cl}); st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. NAVIGAZIONE ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.write(f"Ciao **{st.session_state.user_data['nome']}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME PAGE CON COUNTDOWN ---
if scelta == "🏠 Home":
    st.title("Benvenuta nel Loop ✨")

    # LOGICA TRACKER 90 GIORNI
    if st.session_state.user_data["ha_ordinato"] and st.session_state.user_data["data_ordine"]:
        data_fine = st.session_state.user_data["data_ordine"] + timedelta(days=90)
        oggi = datetime.now()
        giorni_mancanti = (data_fine - oggi).days
        giorni_passati = 90 - giorni_mancanti
        
        if giorni_mancanti > 7:
            st.markdown(f"""
            <div class="tracker-box">
                <p style="margin-bottom:5px;">📅 <b>Il tuo Loop: Giorno {giorni_passati} di 90</b></p>
                <p style="font-size:0.9em;">Mancano <b>{giorni_mancanti} giorni</b> al tuo cambio taglia.</p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(giorni_passati / 90, 1.0))
        elif 0 <= giorni_mancanti <= 7:
            st.markdown(f"""
            <div class="alert-scadenza">
                🔔 NOTIFICA: Mancano solo {giorni_mancanti} giorni!<br>
                Prepariamo la nuova taglia? 📦
            </div>
            """, unsafe_allow_html=True)
            if st.button("SÌ, CAMBIAMO TAGLIA! 🚀"): st.success("Richiesta inviata!")

    st.markdown("""<div class="vision-card"><h4>Cos'è LoopBaby? 🌿</h4><p>L'armadio che cresce col tuo bimbo. Risparmi spazio e oltre 1.000€ l'anno.</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><b>{st.session_state.iscritti} / 50 posti occupati</b></div>""", unsafe_allow_html=True)

# --- 7. BOX STANDARD (ATTIVA IL COUNTDOWN) ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19€)")
    st.write("Scegli lo stile e attiva il tuo Loop di 90 giorni:")
    for s in ["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"]:
        with st.expander(f"🔍 Dettagli {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s):
            st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
            st.success(f"Ordine {s} confermato! Inizia il tuo viaggio di 90 giorni.")

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    st.subheader(f"Mamma: {st.session_state.user_data['nome']}")
    if st.session_state.user_data["ha_ordinato"]:
        st.write(f"Data inizio Loop: **{st.session_state.user_data['data_ordine'].strftime('%d/%m/%Y')}**")
        st.info("Nella Home trovi il countdown aggiornato ogni giorno!")
    else:
        st.warning("Non hai ancora un Loop attivo. Ordina la tua prima Box!")

# --- 9. ADMIN ---
elif scelta == "🔐 Admin":
    st.title("Gestione 🔐")
    st.write(f"Iscritti: {st.session_state.iscritti}")
    if st.session_state.user_data["cellulare"]:
        msg = urllib.parse.quote(f"Ciao {st.session_state.user_data['nome']}! 😊")
        st.markdown(f'<a href="https://wa.me{st.session_state.user_data["cellulare"]}?text={msg}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:10px; border-radius:10px; width:100%;">📲 WHATSAPP</button></a>', unsafe_allow_html=True)

# (Section Premium and Vetrina kept standard)
