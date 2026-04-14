import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- STILE GRAFICO (CSS PULITO) ---
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa; max-width: 500px; margin: 0 auto; }
    .stButton>button { border-radius: 25px; height: 3.5em; font-weight: bold; background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); color: white; border: none; width: 100%; }
    .step-box { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; min-height: 270px; display: flex; flex-direction: column; justify-content: center; }
    .step-box h3 { color: #0d9488; font-size: 1.1em; font-weight: 900; margin-bottom: 5px; }
    .step-box p { color: #333; font-size: 0.85em; font-weight: 600; line-height: 1.2; }
    .promo-card { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 20px; border-radius: 20px; border: 2px solid #d97706; margin-bottom: 20px; color: #92400e; text-align: center; }
    .alert-scadenza { background-color: #fef3c7; border-left: 10px solid #d97706; padding: 20px; border-radius: 15px; color: #92400e; font-weight: bold; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 25px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .vision-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now()}
if "iscritti" not in st.session_state: st.session_state.iscritti = 12

# --- LOGIN ---
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
        nm = st.text_input("Nome")
        nb = st.text_input("Nome Bimbo")
        pb = st.number_input("Peso (kg)", 2.0, 20.0, 5.0)
        tg = "0-1m" if pb < 4.5 else "1-3m" if pb < 5.5 else "3-6m" if pb < 7.5 else "6-9m" if pb < 9.0 else "12-24m"
        if st.button("REGISTRATI"):
            if nm: st.session_state.user_data = {"nome": nm, "bimbo": nb, "taglia": tg, "data_ordine": datetime.now()}; st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- MENU ---
with st.sidebar:
    st.title("🧸 LoopBaby")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Admin")
    scelta = st.radio("Vai a:", menu)
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- SEZIONI ---
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10: st.markdown(f'<div class="alert-scadenza">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg, cambiamo taglia? 📦</div>', unsafe_allow_html=True)
    st.markdown('<div class="vision-card"><h4 style="color: #0d9488; margin-top:0;">Cos\'è LoopBaby? 🌿</h4><p>L\'armadio circolare: risparmi oltre 1.000€ l\'anno e liberi spazio in casa.</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><p>Ritiro GRATIS e 1° BOX OMAGGIO!</p><div style="font-weight:bold;">{st.session_state.iscritti} / 50 posti</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="costi-card"><h4>💰 Tariffe e Resi</h4><ul><li>🏷️ Box Standard: 19€ | 💎 Premium: 29€</li><li>🔄 Reso GRATIS se rinnovi | ⏳ Durata: 3 mesi</li></ul></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota l\'armadio: spedisci 10+ capi.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>10 capi igienizzati: il fabbisogno ideale.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi entro 3 mesi per il cambio taglia!</p></div>', unsafe_allow_html=True)

elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard")
    for s, d in {"🌙 LUNA": "Pastello", "☀️ SOLE": "Vivace", "☁️ NUVOLA": "Casual"}.items():
        with st.expander(f"🔍 Vedi {s}"):
            st.write(d)
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s): st.session_state.user_data["data_ordine"] = datetime.now(); st.success("Ordine inviato!")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    if st.button("ORDINA PREMIUM"): st.session_state.user_data["data_ordine"] = datetime.now(); st.success("Richiesta inviata!")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra")

elif scelta == "🔐 Admin":
    st.title("🔐 Admin"); st.write(f"Iscritti: {st.session_state.iscritti}"); st.write(st.session_state.user_data)
