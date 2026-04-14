import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE E BLOCCO GRAFICO (STILE APP) ---
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="🧸", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS PROFESSIONALE (BLOCCO ZOOM E MOBILE FIRST) ---
st.markdown("""
    <style>
    /* Nasconde elementi tecnici di Streamlit */
    header, footer, #MainMenu {visibility: hidden;}
    
    /* Blocca la visualizzazione stile App su Mobile */
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    
    /* Pulsanti Moderni */
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
    .savings-text { text-align: center; color: #065f46; font-weight: bold; font-size: 1.1em; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIONE DATI E SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire", "data_ordine": datetime.now()}
if "iscritti" not in st.session_state: st.session_state.iscritti = 12

# --- 3. SCHERMATA LOGIN / REGISTRAZIONE (BLOCCANTE) ---
if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA NELL'APP"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
    
    with t2:
        st.write("### Diventa Mamma Fondatrice")
        nm = st.text_input("Il tuo Nome")
        nb = st.text_input("Nome del tuo Bimbo/a")
        pb = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        tg = "0-1m" if pb < 4.5 else "1-3m" if pb < 5.5 else "3-6m" if pb < 7.5 else "6-9m" if pb < 9.0 else "12-24m"
        if st.button("REGISTRATI ORA"):
            if nm: 
                st.session_state.user_data = {"nome": nm, "bimbo": nb, "taglia": tg, "data_ordine": datetime.now()}
                st.session_state.autenticato = "utente"
                st.session_state.iscritti += 1
                st.rerun()
    st.stop()

# --- 4. MENU LATERALE ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=100)
    else: st.title("🧸 Menu")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Area Admin")
    scelta = st.radio("Naviga:", menu)
    if st.button("Esci dall'account"): st.session_state.autenticato = False; st.rerun()

# --- 5. SEZIONI ---

if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    # ALERT 10 GIORNI (Notifica Cambio Taglia)
    scad = st.session_state.user_data["data_ordine"] + timedelta(days=90)
    res = (scad - datetime.now()).days
    if 0 <= res <= 10:
        st.markdown(f'<div class="promo-card" style="background:#fff1f2; border-color:#e11d48; color:#e11d48;">🔔 Ciao {st.session_state.user_data["nome"]}, mancano {res} gg, cambiamo taglia? 📦</div>', unsafe_allow_html=True)

    # COS'È LOOPBABY
    st.markdown("""
    <div class="vision-card">
        <h4 style="color: #0d9488; margin-top:0;">Cos'è LoopBaby? 🌿</h4>
        <p>L'armadio circolare intelligente: <b>risparmi oltre 1.000€ l'anno</b> e liberi spazio in casa seguendo la crescita del tuo bambino passo dopo passo.</p>
    </div>
    """, unsafe_allow_html=True)

    # 3 BOX STEP
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota il tuo armadio: spedisci 10 o più capi al Locker più vicino.</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>Scegli una box da 10 capi igienizzati e stirati: il fabbisogno settimanale ideale.</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Usali e rendili entro 3 mesi per il cambio taglia! Reso gratis se rinnovi.</p></div>', unsafe_allow_html=True)

    # PROMO FONDATRICI
    st.markdown(f'<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Gratis e 1° Box OMAGGIO!<br><b>{st.session_state.iscritti}/50 posti occupati</b></div>', unsafe_allow_html=True)

    # TARIFFE
    st.markdown("""
    <div class="costi-card">
        <h4>💰 Tariffe e Resi</h4>
        <ul>
            <li>🏷️ <b>Box Standard: 19,00 €</b> (Sped. Inclusa)</li>
            <li>💎 <b>Box Premium: 29,00 €</b> (Sped. Inclusa)</li>
            <li>🚛 <b>Vetrina:</b> Spedizione OMAGGIO sopra i 50,00 €</li>
            <li>🔄 <b>Reso GRATIS:</b> Se rinnovi la box</li>
            <li>🎟️ <b>Reso Singolo:</b> Ticket a 7,90 €</li>
            <li>⏳ <b>Durata:</b> Reso entro 3 mesi</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="savings-text">💰 Risparmio Annuale stimato per te: ~1.048 €</div>', unsafe_allow_html=True)

elif scelta == "📝 Profilo Bimbo":
    st.title("📝 Profilo Bimbo")
    st.write(f"Nome del bambino: **{st.session_state.user_data['bimbo']}**")
    st.write(f"Taglia attuale calcolata: **{st.session_state.user_data['taglia']}**")

elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Box Standard (19€)")
    st.info("Sanificazione professionale a vapore garantita.")
    for s, d in {"🌙 LUNA": "Colori delicati e tessuti pastello", "☀️ SOLE": "Colori vivaci e stampe allegre", "☁️ NUVOLA": "Look casual e pratico"}.items():
        st.markdown(f"### {s}")
        st.write(d)
        with st.expander(f"🔍 Vedi Foto e Dettagli {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s): 
            st.session_state.user_data["data_ordine"] = datetime.now()
            st.success(f"Ordine {s} inviato! Il tuo Loop di 3 mesi riparte oggi.")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29€)")
    st.write("Grandi firme selezionate (Nike, Adidas, Ralph Lauren...)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    if st.button("ORDINA PREMIUM"): 
        st.session_state.user_data["data_ordine"] = datetime.now()
        st.balloons(); st.success("Richiesta Premium inviata!")

elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.info("Spedizione GRATIS sopra i 50€! Capi da tenere per sempre.")
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg"); st.button("Compra Scarpe", key="v1")
    with col2:
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg"); st.button("Compra Set", key="v2")

elif scelta == "🔐 Area Admin":
    st.title("🔐 Pannello Admin")
    st.write(f"Iscritti totali: **{st.iscritti}**")
    st.write("Dati ultima sessione:", st.session_state.user_data)
