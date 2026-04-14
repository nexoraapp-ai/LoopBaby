import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE (Menu visibile e ottimizzato) ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="🧸", 
    layout="centered",
    initial_sidebar_state="auto"
)

# --- 2. STILE GRAFICO PROFESSIONALE (PC & MOBILE) ---
st.markdown("""
    <style>
    /* Rende visibile il tasto con le 3 linee (Menu Hamburger) */
    .st-emotion-cache-12fmjuu { color: #0d9488 !important; }
    
    /* Nasconde solo il footer e il menu tecnico di destra, lascia le 3 linee a sinistra */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Sfondo e larghezza fissa stile App */
    .stApp { 
        background-color: #f0fdfa !important; 
        max-width: 500px; 
        margin: 0 auto; 
    }
    
    /* Pulsanti "Loop" */
    .stButton>button { 
        border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important; 
        color: white !important; border: none !important; width: 100% !important; 
    }
    
    /* Box Passaggi Home */
    .step-box { 
        background-color: white !important; padding: 20px; border-radius: 20px; 
        border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; 
        min-height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; margin-bottom: 10px; }
    .step-box p { color: #333; font-size: 0.95em; line-height: 1.3; font-weight: 600; }
    
    /* Card Speciali */
    .promo-card { background-color: #fef3c7 !important; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .vision-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .alert-scadenza { background-color: #fef3c7; border-left: 10px solid #d97706; padding: 15px; border-radius: 10px; color: #92400e; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GESTIONE SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now() - timedelta(days=82)}
if "iscritti" not in st.session_state: st.session_state.iscritti = 12

# --- 4. LOGIN / REGISTRAZIONE ---
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

# --- 5. MENU LATERALE (Con le 3 linee) ---
with st.sidebar:
    st.title("🧸 LoopBaby")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Area Admin")
    scelta = st.radio("Navigazione:", menu)
    if st.button("Esci dall'account"): st.session_state.autenticato = False; st.rerun()

# --- 6. SEZIONI ---

if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    # Notifica Scadenza (10 giorni)
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10:
        st.markdown(f'<div class="alert-scadenza">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg, cambiamo taglia?</div>', unsafe_allow_html=True)

    st.markdown("""<div class="vision-card"><h4>Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare intelligente: <b>risparmi oltre 1.000€ l'anno</b> e liberi spazio in casa.</p></div>""", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a: st.markdown('<div class="step-box"><h3>📦 Inviaci i tuoi capi</h3><p>Svuota l\'armadio: spedisci 10+ capi al Locker.</p></div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>10 capi igienizzati e stirati: il fabbisogno ideale.</p></div>', unsafe_allow_html=True)
    with col_c: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi entro 3 mesi per il cambio taglia! Reso gratis se rinnovi.</p></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Gratis e 1° Box OMAGGIO!<br><b>{st.session_state.iscritti}/50 posti occupati</b></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="costi-card"><h4>💰 Tariffe e Resi</h4><ul><li>🏷️ Box Standard: 19€ (Sped. Inclusa)</li><li>💎 Premium: 29€ | ⏳ Durata: 3 mesi</li><li>🔄 Reso GRATIS se rinnovi | 🚛 Vetrina: gratis > 50€</li></ul></div>', unsafe_allow_html=True)

elif scelta == "📝 Profilo Bimbo":
    st.title("👤 Profilo Bimbo")
    st.write(f"Nome: **{st.session_state.user_data['bimbo']}**")
    st.write(f"Taglia: **{st.session_state.user_data['taglia']}**")

elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard")
    st.write("---")
    for s, d in {"🌙 LUNA": "Colori delicati e pastello", "☀️ SOLE": "Colori vivaci e allegre", "☁️ NUVOLA": "Casual e pratico"}.items():
        st.markdown(f"### {s}")
        with st.expander(f"🔍 Vedi Foto {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s): st.success(f"Ordine {s} ricevuto!")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29€)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("ORDINA PREMIUM")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.info("Spedizione GRATIS sopra i 50€!")
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra Scarpe", key="v1")
    with col2:
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg"); st.button("Compra Set", key="v2")

elif scelta == "🔐 Area Admin":
    st.title("🔐 Admin"); st.write(f"Iscritti: {st.session_state.iscritti}")
