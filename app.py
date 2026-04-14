import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- 2. STILE GRAFICO (CSS) ---
st.markdown("""
    <style>
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    .stButton>button { border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important; color: white !important; border: none !important; width: 100% !important; }
    .step-box { background-color: white !important; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; min-height: 250px; display: flex; flex-direction: column; justify-content: center; }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; }
    .promo-card { background-color: #fef3c7 !important; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .nota-rossa { color: #e11d48; font-weight: bold; font-size: 0.9em; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now()}
if "iscritti" not in st.session_state: st.session_state.iscritti = 12

# --- 4. LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    with tab1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    with tab2:
        st.write("### Diventa Mamma Fondatrice")
        nm = st.text_input("Il tuo Nome")
        if st.button("REGISTRATI ORA"):
            if nm: st.session_state.user_data["nome"] = nm; st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. MENU ---
with st.sidebar:
    st.title("🧸 Menu")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME ---
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    # 3 BOX STEP
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota l\'armadio: spedisci 10+ capi al Locker.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>Scegli una box da 10 capi igienizzati e stirati.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi i capi per il cambio taglia o acquistali!</p></div>', unsafe_allow_html=True)

    # PROMO FONDATRICI
    st.markdown(f"""
    <div class="promo-card">
        <h2 style="margin-bottom:5px;">🚀 PROMO FONDATRICI</h2>
        <p><b>Ritiro Locker GRATIS e 1° BOX OMAGGIO</b><br>riservato alle prime 50 mamme che inviano 10 o più capi!</p>
        <div style="font-size:1.2em; font-weight:bold;">{st.session_state.iscritti} / 50 posti occupati</div>
    </div>
    """, unsafe_allow_html=True)

    # TARIFFE
    st.markdown("""
    <div class="costi-card">
        <h4 style="color: #0d9488; margin-top:0;">💰 Tariffe e Spedizioni</h4>
        <ul style="margin-bottom:0;">
            <li>🏷️ <b>Box Standard: 19,00 €</b> (Spedizione Inclusa)</li>
            <li>💎 <b>Box Premium: 29,00 €</b> (Spedizione Inclusa)</li>
            <li>🔄 <b>Reso GRATIS</b> se ordini una nuova Box</li>
            <li>🚛 <b>Vetrina:</b> Spedizione GRATUITA sopra i 50,00 €</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p class="nota-rossa">⚠️ Ricorda: i capi vanno resi entro un massimo di 3 mesi.</p>', unsafe_allow_html=True)

# --- 7. BOX STANDARD ---
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19€)")
    for s in ["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"]:
        with st.expander(f"🔍 Vedi Foto {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button(f"Ordina {s} - 19€", key=s)

# --- 8. BOX PREMIUM ---
elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29€)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("ORDINA PREMIUM - 29€")

# --- 9. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.success("✨ Capi da tenere per sempre: NO RESO OBBLIGATORIO")
    st.info("🚚 Spedizione GRATUITA per ordini superiori a 50,00 €")
    if os.path.exists("scarpe.jpg"): 
        st.image("scarpe.jpg", caption="Esempio Scarpe Firmate")
        st.button("Aggiungi al carrello")
