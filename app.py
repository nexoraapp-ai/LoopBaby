import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE E BLOCCO TOTALE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- CSS PER BLOCCARE L'APP STILE INSTAGRAM ---
st.markdown("""
    <style>
    /* Blocca lo zoom e il movimento laterale per farlo sembrare un'app vera */
    header, footer, #MainMenu {visibility: hidden;}
    
    .stApp { 
        background-color: #f0fdfa; 
        max-width: 500px; 
        margin: 0 auto; 
    }

    /* Pulsanti bloccati e moderni */
    .stButton>button { 
        border-radius: 25px; height: 3.5em; font-weight: bold; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); 
        color: white; border: none; width: 100%; 
    }

    .step-box { background: white; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; }
    .promo-card { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 20px; border-radius: 20px; border: 2px solid #d97706; color: #92400e; text-align: center; }
    .costi-card { background: #fff1f2; padding: 25px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: st.session_state.user_data = {"nome": "Mamma", "data_ordine": datetime.now()}
if "iscritti" not in st.session_state: st.session_state.iscritti = 12

# LOGIN / REGISTRAZIONE
if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        nm = st.text_input("Il tuo Nome")
        if st.button("REGISTRATI ORA"):
            if nm: st.session_state.user_data["nome"] = nm; st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# MENU LATERALE
with st.sidebar:
    st.title("🧸 Menu")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Admin")
    scelta = st.radio("Vai a:", menu)
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# CONTENUTO HOME
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f'<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro GRATIS e 1° BOX OMAGGIO!</p><b>{st.session_state.iscritti} / 50 posti occupati</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="costi-card"><h4>💰 Tariffe e Resi</h4><ul><li>🏷️ Box Standard: 19€ | ⏳ Durata: 3 mesi</li><li>🔄 Reso GRATIS se rinnovi</li></ul></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota l\'armadio: 10+ capi.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>10 capi igienizzati.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Entro 3 mesi per il cambio tg!</p></div>', unsafe_allow_html=True)

# ALTRE PAGINE (Standard, Premium, Vetrina)
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard")
    for s, d in {"🌙 LUNA": "Pastello", "☀️ SOLE": "Vivace", "☁️ NUVOLA": "Casual"}.items():
        with st.expander(f"🔍 Vedi {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button(f"Ordina {s}", key=s)

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("ORDINA PREMIUM")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("Compra e tieni")

elif scelta == "🔐 Admin":
    st.title("🔐 Area Admin"); st.write(f"Iscritti totali: {st.session_state.iscritti}")
