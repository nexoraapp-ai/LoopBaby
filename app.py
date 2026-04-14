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
        background-color: #ffffff; padding: 20px; border-radius: 20px; 
        border: 3px solid #0d9488; text-align: center; margin-bottom: 15px; 
        min-height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    .step-box h3 { color: #0d9488; font-size: 1.2em; font-weight: 900; margin-bottom: 10px; }
    .step-box p { color: #333; font-size: 0.95em; line-height: 1.3; font-weight: 600; }
    
    .promo-card { 
        background-color: #e0f2fe; padding: 20px; border-radius: 20px; 
        border-left: 10px solid #0369a1; margin-bottom: 20px; color: #0c4a6e; 
    }
    .costi-card {
        background-color: #fff1f2; padding: 20px; border-radius: 15px;
        border: 2px solid #e11d48; color: #333; margin-bottom: 20px;
    }
    .savings-text { 
        text-align: center; color: #065f46; font-weight: bold; 
        font-size: 1.2em; margin-top: 30px; padding: 10px; border-top: 1px solid #0d9488;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIONE SESSIONE ---
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {"nome": "Mamma", "bimbo": "", "taglia": "da definire"}

# --- LOGIN / REGISTRAZIONE ---
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
        n_mamma = st.text_input("Il tuo Nome")
        n_bimbo = st.text_input("Nome del Bimbo/a")
        p_bimbo = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        t = "0-1m" if p_bimbo < 4.5 else "1-3m" if p_bimbo < 5.5 else "3-6m" if p_bimbo < 7.5 else "6-9m" if p_bimbo < 9.0 else "12-24m"
        if st.button("REGISTRATI E INIZIA"):
            if n_mamma:
                st.session_state.user_data = {"nome": n_mamma, "bimbo": n_bimbo, "taglia": t}
                st.session_state.autenticato = "utente"
                st.rerun()
    st.stop()

# --- MENU ---
with st.sidebar:
    st.title("🧸 LoopBaby")
    st.write(f"Ciao, **{st.session_state.user_data['nome']}**!")
    menu = ["🏠 Home", "📝 Profilo Bimbo", "📦 Box Standard (19€)", "💎 Box Premium (29€)", "🛍️ Vetrina"]
    if st.session_state.autenticato == "admin": menu.append("🔐 Area Admin")
    scelta = st.sidebar.radio("Naviga:", menu)
    if st.button("Esci"):
        st.session_state.autenticato = False
        st.rerun()

# --- SEZIONI ---

if scelta == "🏠 Home":
    st.markdown(f"### Benvenuta {st.session_state.user_data['nome']}! ✨")
    
    # --- COS'È LOOPBABY ---
    with st.container():
        st.markdown("""
        <div style="background-color: #ffffff; padding: 20px; border-radius: 20px; margin-bottom: 20px; border: 1px solid #0d9488;">
            <h4 style="color: #0d9488;">Cos'è LoopBaby?</h4>
            <p>È la prima app di <b>Moda Circolare</b> dedicata ai più piccoli. Un sistema intelligente che ti permette di avere un armadio sempre perfetto, senza sprechi di soldi e spazio.</p>
            <p><b>Come funziona:</b> Scegli la tua Box, ricevi i capi igienizzati, usali finché il bimbo cresce e rendili per ricevere la taglia successiva.</p>
        </div>
        """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="step-box"><h3>📦 Inviaci i tuoi capi</h3><p>Svuota l\'armadio: spedisci 10 o più capi al Locker più vicino a te.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="step-box"><h3>🚚 Ricevi la Box</h3><p>Scegli una box da 10 capi igienizzati e stirati per il tuo bimbo.</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="step-box"><h3>🔄 Usa e Rendi</h3><p>Usali e rendili entro 3 mesi o al cambio taglia! Reso gratis se rinnovi.</p></div>', unsafe_allow_html=True)

    # --- COSTI E REGOLE ---
    st.markdown("""
    <div class="costi-card">
        <h4 style="color: #e11d48;">💰 Costi e Spedizioni</h4>
        <ul>
            <li><b>Box Standard: 19,00 €</b> (Spedizione Inclusa).</li>
            <li><b>Reso GRATIS:</b> Se ordini una nuova box di valore pari o superiore.</li>
            <li><b>Reso Singolo:</b> Se vuoi solo rendere senza riordinare, inviamo noi un ticket al costo di <b>7,90 €</b>.</li>
            <li><b>Durata:</b> I capi vanno resi entro un massimo di <b>3 mesi</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> Ritiro Locker GRATIS e PRIMA BOX OMAGGIO!</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="savings-text">💰 Risparmio Annuale stimato per te: ~1.048 €</div>', unsafe_allow_html=True)

elif scelta == "📝 Profilo Bimbo":
    st.title("👤 Profilo di " + st.session_state.user_data['bimbo'])
    st.write(f"**Taglia attuale:** {st.session_state.user_data['taglia']}")
    st.info("La taglia viene aggiornata automaticamente quando inserisci il peso nel prossimo ordine.")

elif scelta == "📦 Box Standard (19€)":
    st.title("📦 Scegli la tua Box Standard")
    st.write(f"Taglia per {st.session_state.user_data['bimbo']}: **{st.session_state.user_data['taglia']}**")
    st.warning("⏳ I capi vanno restituiti entro 3 mesi o prima al cambio taglia.")
    st.write("---")

    # --- BOX LUNA ---
    with st.container():
        st.markdown("### 🌙 Tipologia LUNA")
        st.write("Stile delicato, tessuti morbidi e colori pastello.")
        with st.expander("🔍 Vedi Foto e Dettagli Luna"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button("Ordina LUNA - 19€", key="btn_luna"):
            st.success("Hai ordinato la Box Luna! Spedizione a nostro carico.")

    st.write("---")

    # --- BOX SOLE ---
    with st.container():
        st.markdown("### ☀️ Tipologia SOLE")
        st.write("Colori vivaci, stampe allegre e tessuti resistenti.")
        with st.expander("🔍 Vedi Foto e Dettagli Sole"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button("Ordina SOLE - 19€", key="btn_sole"):
            st.success("Hai ordinato la Box Sole! Spedizione a nostro carico.")

    st.write("---")

    # --- BOX NUVOLA ---
    with st.container():
        st.markdown("### ☁️ Tipologia NUVOLA")
        st.write("Look casual, pratico e colori neutri per ogni giorno.")
        with st.expander("🔍 Vedi Foto e Dettagli Nuvola"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button("Ordina NUVOLA - 19€", key="btn_nuvola"):
            st.success("Hai ordinato la Box Nuvola! Spedizione a nostro carico.")

elif scelta == "💎 Box Premium (29€)":
    st.title("💎 Box Premium (29€)")
    st.write("Grandi firme selezionate (Nike, Adidas, Ralph Lauren...)")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
    st.button("Ordina Premium")

elif scelta == "🛍️ Vetrina Acquisto":
    st.title("🛍️ Vetrina Acquisto")
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
        st.button("Compra", key="v1")
    with col2:
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.button("Compra", key="v2")

elif scelta == "🔐 Area Admin":
    st.title("🔐 Pannello Admin")
    st.write("**Mamme iscritte:**")
    st.write(st.session_state.user_data)
