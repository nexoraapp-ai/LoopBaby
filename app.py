import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="🧸", layout="centered")

# --- STILE GRAFICO (CSS) ---
st.markdown("""
    <style>
    header, footer, #MainMenu {visibility: hidden;}
    .stApp { background-color: #f0fdfa; }
    .stButton>button { 
        border-radius: 25px; height: 3.5em; font-weight: bold; 
        background: linear-gradient(135deg, #0d9488 0%, #0369a1 100%); 
        color: white; border: none; width: 100%; 
    }
    .step-box { 
        background-color: #ffffff; padding: 15px; border-radius: 20px; 
        border: 2px solid #0d9488; text-align: center; margin-bottom: 10px; 
    }
    .step-box h3 { color: #0d9488; font-size: 1.1em; font-weight: 900; margin-bottom: 5px; }
    .step-box p { color: #333; font-size: 0.85em; line-height: 1.2; font-weight: 600; }
    
    .promo-card { 
        background-color: #e0f2fe; padding: 20px; border-radius: 20px; 
        border-left: 10px solid #0369a1; margin-bottom: 20px; color: #0c4a6e; 
    }
    .savings-text { 
        text-align: center; color: #065f46; font-weight: bold; 
        font-size: 1.1em; margin-top: 20px; padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIONE SESSIONE (LOGIN E DATI) ---
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire"}

# --- SCHERMATA LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    st.markdown("<h2 style='text-align: center; color: #0d9488;'>🧸 LoopBaby</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Accedi", "Registrati"])
    
    with tab1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024":
                st.session_state.autenticato = "admin"
                st.rerun()
            elif e:
                st.session_state.autenticato = "utente"
                st.rerun()
    
    with tab2:
        st.write("### Crea il tuo account")
        nome_mamma = st.text_input("Il tuo Nome")
        nome_bimbo = st.text_input("Nome del Bimbo/a")
        peso_bimbo = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        email_reg = st.text_input("Email di registrazione")
        pwd_reg = st.text_input("Scegli Password", type="password")
        
        # Calcolo taglia automatico
        taglia = "0-1m" if peso_bimbo < 4.5 else "1-3m" if peso_bimbo < 5.5 else "3-6m" if peso_bimbo < 7.5 else "6-9m" if peso_bimbo < 9.0 else "12-24m"
        
        if st.button("REGISTRATI E INIZIA"):
            if nome_mamma and email_reg:
                st.session_state.user_data = {"nome": nome_mamma, "bimbo": nome_bimbo, "taglia": taglia}
                st.session_state.autenticato = "utente"
                st.success("Registrazione completata!")
                st.rerun()
    st.stop()

# --- MENU LATERALE ---
with st.sidebar:
    st.title("🧸 LoopBaby")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin":
        menu.append("🔐 Area Admin")
    scelta = st.sidebar.radio("Naviga:", menu)
    if st.button("Esci"):
        st.session_state.autenticato = False
        st.rerun()

# --- SEZIONI ---

# 1. HOME
if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.subheader("La moda circolare da 0 a 24 mesi.")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="step-box"><h3>📦 Inviaci i capi</h3><p>Svuota l\'armadio e spedisci 10 o più capi.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>Al Locker più vicino a te della tua taglia.</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="step-box"><h3>🔄 Scambia</h3><p>Rendi o acquista quando cresce!</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Locker GRATIS e PRIMA BOX OMAGGIO!</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="savings-text">💰 Risparmio Annuale stimato per te: ~1.048 €</div>', unsafe_allow_html=True)

# 2. PROFILO BIMBO
elif scelta == "📝 Profilo Bimbo":
    st.title("👤 Profilo del Bimbo")
    st.write(f"**Nome:** {st.session_state.user_data['bimbo']}")
    st.write(f"**Taglia attuale:** {st.session_state.user_data['taglia']}")
    st.info("La taglia viene aggiornata automaticamente in base al peso inserito in fase di ordine.")

# 3. BOX STANDARD
elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Scegli la tua Box")
    st.write(f"Taglia selezionata per **{st.session_state.user_data['bimbo']}**: **{st.session_state.user_data['taglia']}**")
    st.warning("⏳ La box è tua per 3 mesi. Ti avviseremo 10 giorni prima della scadenza!")
    
    tab_luna, tab_sole, tab_nuvola = st.tabs(["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"])
    
    with tab_luna:
        st.write("**Stile:** Colori delicati e tessuti pastello.")
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button("Ordina Luna - 19€", key="l1")
        
    with tab_sole:
        st.write("**Stile:** Colori vivaci e stampe allegre.")
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button("Ordina Sole - 19€", key="s1")
        
    with tab_nuvola:
        st.write("**Stile:** Look casual e pratico per ogni giorno.")
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button("Ordina Nuvola - 19€", key="n1")

# 4. PREMIUM
elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29€)")
    st.write("Grandi firme selezionate (Nike, Adidas, ecc.)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("Ordina Premium - 29€")

# 5. VETRINA
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.info("I capi in questa sezione sono tuoi per sempre.")
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg", caption="Scarpe Firmate")
        st.button("Compra ora", key="v1")
    with col2:
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg", caption="Set coordinato")
        st.button("Compra ora", key="v2")

# 6. ADMIN
elif scelta == "🔐 Area Admin":
    st.title("Admin")
    st.write("Dati Iscritti:")
    st.write(st.session_state.user_data)
