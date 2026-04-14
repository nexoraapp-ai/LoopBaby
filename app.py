import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE (Menu ora visibile) ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="🧸", 
    layout="centered"
)

# --- CSS PROFESSIONALE ---
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    .stButton>button { 
        border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important; 
        color: white !important; border: none !important; width: 100% !important; 
    }
    .step-box { 
        background-color: white !important; padding: 20px; border-radius: 20px; 
        border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; 
        min-height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; }
    .step-box p { color: #333; font-size: 0.95em; line-height: 1.3; font-weight: 600; }
    .promo-card { background-color: #fef3c7 !important; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .vision-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIONE SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now()}
if "iscritti" not in st.session_state: st.session_state.iscritti = 12

# --- 3. LOGIN / REGISTRAZIONE ---
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
        st.write("### Diventa Mamma Fondatrice")
        nm = st.text_input("Il tuo Nome")
        nb = st.text_input("Nome Bimbo/a")
        pb = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        tg = "0-1m" if pb < 4.5 else "1-3m" if pb < 5.5 else "3-6m" if pb < 7.5 else "6-9m" if pb < 9.0 else "12-24m"
        if st.button("REGISTRATI ORA"):
            if nm: 
                st.session_state.user_data = {"nome": nm, "bimbo": nb, "taglia": tg, "data_ordine": datetime.now()}
                st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 4. MENU LATERALE ---
with st.sidebar:
    st.title("🧸 Menu")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Area Admin")
    scelta = st.radio("Scegli sezione:", menu)
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 5. SEZIONI ---
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    # Notifica Scadenza
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10:
        st.markdown(f'<div class="promo-card" style="background:#fff1f2; border-color:#e11d48; color:#e11d48;">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg, cambiamo taglia?</div>', unsafe_allow_html=True)

    st.markdown("""<div class="vision-card"><h4>Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare intelligente: <b>risparmi oltre 1.000€ l'anno</b> e liberi spazio in casa.</p></div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota l\'armadio: spedisci 10+ capi al Locker.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>Scegli una box da 10 capi igienizzati.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi entro 3 mesi per il cambio taglia!</p></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Gratis e 1° Box OMAGGIO!<br><b>{st.session_state.iscritti}/50 posti</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="costi-card"><h4>💰 Tariffe e Resi</h4><ul><li>🏷️ Box Standard: 19€ | 💎 Premium: 29€</li><li>🔄 Reso GRATIS se rinnovi | ⏳ Durata: 3 mesi</li></ul></div>', unsafe_allow_html=True)

elif scelta == "📝 Profilo Bimbo":
    st.title("📝 Profilo")
    st.write(f"Bimbo: {st.session_state.user_data['bimbo']}")
    st.write(f"Taglia: {st.session_state.user_data['taglia']}")

elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard")
    for s, d in {"🌙 LUNA": "Pastello", "☀️ SOLE": "Vivace", "☁️ NUVOLA": "Casual"}.items():
        st.markdown(f"### {s}")
        with st.expander(f"🔍 Vedi Foto"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button(f"Ordina {s}", key=s)

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("ORDINA PREMIUM")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra")
