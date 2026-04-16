import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, p, span, label, div { color: #0d9488 !important; }
    
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    .vision-card, .card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .tracker-box { background: #eef2ff; padding: 15px; border-radius: 20px; border: 2px solid #4338ca; margin-bottom: 20px; text-align: center; }
    .suggested-tag { font-size: 1.5em; font-weight: bold; color: #e11d48; background: #fff1f2; padding: 10px; border-radius: 10px; display: inline-block; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "bimbo": "", "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire",
        "taglia_confermata": False
    }

def calcola_tg(peso):
    if peso < 4.5: return "0-1m"
    elif peso < 5.5: return "1-3m"
    elif peso < 7.5: return "3-6m"
    elif peso < 9.0: return "6-9m"
    else: return "12-24m"

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
        st.info("**Perché scegliere LoopBaby? 🌿**\n\n- Risparmi oltre 1.000€ l'anno\n- Capi igienizzati e pronti all'uso\n- Riduci gli sprechi e liberi spazio in casa")
        n_m = st.text_input("Nome Mamma")
        c_m = st.text_input("N° Telefono")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0)
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and c_m:
                st.session_state.user_data.update({"nome": n_m, "bimbo": n_b, "cellulare": c_m, "peso": p_b, "taglia": calcola_tg(p_b)})
                st.session_state.autenticato = "utente"
                st.session_state.primo_accesso = True
                st.session_state.iscritti += 1
                st.rerun()
    st.stop()

# --- 5. SUGGERIMENTO TAGLIA (POST REGISTRAZIONE) ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h4>Taglia suggerita per {st.session_state.user_data['bimbo']}</h4>
        <div class="suggested-tag">{st.session_state.user_data['taglia']}</div>
        <p>In base al peso di {st.session_state.user_data['peso']} kg</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    if c1.button("✅ CONFERMA"):
        st.session_state.user_data["taglia_confermata"] = True
        st.session_state.primo_accesso = False; st.rerun()
    if c2.button("✏️ MODIFICA"):
        nuova = st.selectbox("Scegli taglia corretta", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.button("SALVA"):
            st.session_state.user_data["taglia"] = nuova
            st.session_state.user_data["taglia_confermata"] = True
            st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    st.write(f"Ciao **{st.session_state.user_data['nome']}**!")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE (CON TRACKER) ---
if scelta == "🏠 Home":
    st.title(f"Bentornata {st.session_state.user_data['nome']}! ✨")

    if st.session_state.user_data["ha_ordinato"]:
        inizio = st.session_state.user_data["data_ordine"]
        giorni_passati = (datetime.now() - inizio).days + 1
        st.markdown(f"""
        <div class="tracker-box">
            <h4>🔄 Loop in corso</h4>
            <h2 style="color:#4338ca !important;">Giorno {giorni_passati} di 90</h2>
            <p>Mancano {90 - giorni_passati} giorni al cambio taglia</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(min(giorni_passati / 90, 1.0))

    st.markdown("""<div class="vision-card"><h4>Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare intelligente. Risparmi, liberi spazio e rispetti il pianeta.</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p><b>{st.session_state.iscritti} / 50 posti occupati</b></p></div>""", unsafe_allow_html=True)

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("p_form"):
        st.write(f"Mamma: **{st.session_state.user_data['nome']}**")
        st.write(f"Bimbo: **{st.session_state.user_data['bimbo']}**")
        st.write(f"Taglia Attiva: **{st.session_state.user_data['taglia']}**")
        st.write(f"Telefono: {st.session_state.user_data['cellulare']}")
        if st.form_submit_button("Modifica Dati"): st.info("Funzione modifica in arrivo!")

# --- 9. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19,90 €)")
    if st.button("ORDINA STANDARD"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
        st.success("Loop attivato! Guarda il tracker in Home.")

# --- 10. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Area Gestione 🔐")
        cel = st.session_state.user_data["cellulare"]
        if cel:
            wa_text = urllib.parse.quote(f"Ciao {st.session_state.user_data['nome']}! Qui LoopBaby, come procede il tuo loop?")
            st.markdown(f'<a href="https://wa.me{cel}?text={wa_text}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%; cursor:pointer;">📲 CONTATTA SU WHATSAPP</button></a>', unsafe_allow_html=True)
            if st.button("🧪 SIMULA +10 GIORNI"):
                if st.session_state.user_data["data_ordine"]:
                    st.session_state.user_data["data_ordine"] -= timedelta(days=10); st.rerun()
    else: st.error("Solo admin!")
