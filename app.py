import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- 2. STILE GRAFICO (CSS) - BLINDATO E MOBILE-FIRST ---
st.markdown("""
    <style>
    /* Interfaccia */
    header {visibility: visible !important;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Pulsanti Instagram Style */
    .stButton>button { 
        border-radius: 25px !important; height: 3.5em !important; font-weight: bold !important; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%) !important; 
        color: white !important; border: none !important; width: 100% !important; 
    }
    
    /* Box e Card */
    .step-box { background-color: white !important; padding: 20px; border-radius: 20px; border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; min-height: 250px; display: flex; flex-direction: column; justify-content: center; }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; margin-bottom: 5px; }
    .step-box p { color: #333; font-size: 0.9em; font-weight: 600; line-height: 1.2; }
    .vision-card { background-color: #ffffff; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background-color: #fef3c7 !important; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; color: #92400e; margin-bottom: 20px; }
    .costi-card { background-color: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; color: #333; margin-bottom: 20px; }
    .alert-scadenza { background-color: #fef3c7; border-left: 10px solid #d97706; padding: 15px; border-radius: 10px; color: #92400e; font-weight: bold; margin-bottom: 15px; }
    .nota-rossa { color: #e11d48; font-weight: bold; font-size: 0.9em; text-align: center; margin-top: -10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INIZIALIZZAZIONE SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now() - timedelta(days=82)}
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
        nb = st.text_input("Nome del Bimbo/a")
        pb = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        tg = "0-1m" if pb < 4.5 else "1-3m" if pb < 5.5 else "3-6m" if pb < 7.5 else "6-9m" if pb < 9.0 else "12-24m"
        if st.button("REGISTRATI ORA"):
            if nm: st.session_state.user_data = {"nome": nm, "bimbo": nb, "taglia": tg, "data_ordine": datetime.now()}; st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. MENU LATERALE ---
with st.sidebar:
    st.title("🧸 LoopBaby")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME PAGE ---
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    # Alert 10 giorni
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10: st.markdown(f'<div class="alert-scadenza">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg, cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    # Vision Card
    st.markdown("""<div class="vision-card"><h4>Cos'è LoopBaby? 🌿</h4><p>L'armadio circolare: <b>risparmi oltre 1.000€ l'anno</b> e liberi spazio in casa seguendo la crescita del tuo bambino. Basta sprechi!</p></div>""", unsafe_allow_html=True)

    # 3 Box Steps
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota l\'armadio: spedisci 10+ capi al Locker.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>Scegli una box da 10 capi igienizzati e stirati.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Rendi entro 3 mesi per il cambio taglia o acquista in Vetrina!</p></div>', unsafe_allow_html=True)

    # Promo e Tariffe
    st.markdown(f'<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Gratis e 1° Box OMAGGIO!<br><b>{st.session_state.iscritti}/50 posti</b></div>', unsafe_allow_html=True)
    st.markdown("""<div class="costi-card"><h4>💰 Tariffe e Spedizioni</h4><ul><li>🏷️ <b>Box Standard: 19,00 €</b> (Spedizione Inclusa)</li><li>💎 <b>Box Premium: 29,00 €</b> (Spedizione Inclusa)</li><li>🔄 <b>Reso GRATIS</b> se ordini una nuova Box</li><li>🚛 <b>Vetrina:</b> Spedizione Omaggio sopra i 50€</li><li>🎟️ <b>Reso Singolo:</b> Ticket a 7,90 €</li></ul></div>""", unsafe_allow_html=True)
    st.markdown('<p class="nota-rossa">⚠️ Ricorda: i capi vanno resi entro un massimo di 3 mesi.</p>', unsafe_allow_html=True)

# --- 7. BOX STANDARD ---
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19€)")
    st.write(f"Taglia per {st.session_state.user_data['bimbo']}: **{st.session_state.user_data['taglia']}**")
    for s, d in {"🌙 LUNA": "Pastello", "☀️ SOLE": "Vivace", "☁️ NUVOLA": "Casual"}.items():
        st.markdown(f"### {s}"); st.write(d)
        with st.expander("🔍 Vedi Foto"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s): st.session_state.user_data["data_ordine"] = datetime.now(); st.success("Ordine inviato! Loop resettato.")

# --- 8. BOX PREMIUM ---
elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium ORO (29€)")
    st.write("Selezione grandi firme (Nike, Adidas, Ralph Lauren...)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    if st.button("ORDINA PREMIUM"): st.balloons(); st.success("Richiesta Premium inviata!")

# --- 9. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.info("Capi da tenere per sempre. Gratis > 50€!")
    col1, col2 = st.columns(2)
    with col1: 
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra Scarpe", key="v1")
    with col2: 
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg"); st.button("Compra Set", key="v2")

# --- 10. PROFILO E ADMIN ---
elif scelta == "📝 Profilo Bimbo":
    st.title("👤 Profilo"); st.write(f"Bimbo: **{st.session_state.user_data['bimbo']}**"); st.write(f"Taglia: **{st.session_state.user_data['taglia']}**")

if st.session_state.autenticato == "admin" and scelta == "🏠 Home":
    st.write("---"); st.write(f"**ADMIN INFO:** Iscritti {st.session_state.iscritti}/50")
