import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO (CSS TOTALE) ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #0d9488 !important; }
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    .vision-card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .costi-card { background: #fff1f2; padding: 20px; border-radius: 20px; border: 2px solid #e11d48; margin-bottom: 20px; }
    .tracker-box { background: white; padding: 15px; border-radius: 20px; border: 2px solid #0d9488; margin-bottom: 20px; text-align: center; }
    .vetrina-item { background: white; padding: 10px; border-radius: 15px; border: 1px solid #ddd; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "Mamma", "bimbo": "", "peso": 5.0, "cell": "", 
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire"
    }

# --- 4. REGISTRAZIONE COMPLETA (PUNTO 1) ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            else: st.session_state.autenticato = "utente"; st.rerun()
    with t2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Tuo Nome e Cognome")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale del bimbo (kg)", 2.0, 20.0, 5.0)
        c_m = st.text_input("Tuo Cellulare")
        if st.button("REGISTRATI ORA"):
            tg = "0-1m" if p_b < 4.5 else "1-3m" if p_b < 5.5 else "3-6m" if p_b < 7.5 else "6-9m" if p_b < 9.0 else "12-24m"
            st.session_state.user_data.update({"nome": n_m, "bimbo": n_b, "peso": p_b, "cell": c_m, "taglia": tg})
            st.session_state.autenticato = "utente"; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. MENU ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=150)
    st.write(f"Ciao **{st.session_state.user_data['nome']}**! 🧸")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 6. HOME PAGE (PUNTO 2 & 3) ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")

    # TRACKER 90 GG
    if st.session_state.user_data["ha_ordinato"]:
        df = st.session_state.user_data["data_ordine"] + timedelta(days=90)
        gm = (df - datetime.now()).days
        st.markdown(f'<div class="tracker-box">📅 <b>Il tuo Loop: Giorno {90-gm} di 90</b><br>Mancano {gm} giorni al cambio taglia.</div>', unsafe_allow_html=True)

    # SPIEGAZIONE LOOPBABY (PUNTO 2)
    st.markdown("""
    <div class="vision-card">
        <h4>Cos'è LoopBaby? 🌿</h4>
        <p>L'armadio intelligente che cresce con il tuo bimbo. <b>Risparmi oltre 1.000€ l'anno!</b></p>
        <p><b>Come funziona:</b><br>
        1. Scegli la tua Box (Standard 19,90€ o Premium 29,90€) con trasporto sempre incluso.<br>
        2. Usala per 3 mesi o cambiala non appena la taglia diventa piccola.<br>
        3. <b>Il Reso:</b> Se ordini la Box successiva, il ritiro della vecchia è <b>GRATIS</b>. Se decidi di non continuare, paghi solo 7,90€ per il ticket di ritiro al Locker sotto casa.</p>
    </div>
    """, unsafe_allow_html=True)

    # PROMO FONDATRICI (PUNTO 3)
    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <p><b>Ritiro Locker GRATIS e 1° BOX OMAGGIO!</b><br>Riservato alle prime 50 mamme. Svuota l'armadio: inviaci 10+ capi usati, l'etichetta la paghiamo noi!</p>
        <div style="font-size:1.3em; font-weight:bold;">{st.session_state.iscritti} / 50 posti occupati</div>
    </div>
    """, unsafe_allow_html=True)

# --- 7. PROFILO (PUNTO 4) ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    st.write(f"**Mamma:** {st.session_state.user_data['nome']}")
    st.write(f"**Bimbo/a:** {st.session_state.user_data['bimbo']}")
    st.write(f"**Taglia consigliata:** {st.session_state.user_data['taglia']}")
    if st.session_state.user_data["ha_ordinato"]:
        st.write(f"**Data inizio Loop:** {st.session_state.user_data['data_ordine'].strftime('%d/%m/%Y')}")

# --- 8. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19,90 €)")
    st.write("10 capi essenziali igienizzati e stirati. Spedizione inclusa!")
    for s in ["🌙 LUNA", "☀️ SOLE", "☁️ NUVOLA"]:
        with st.expander(f"Vedi dettagli {s}"):
            if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        if st.button(f"Ordina {s}", key=s):
            st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
            st.success("Ordine effettuato!")

# --- 9. BOX PREMIUM (PUNTO 5 - ORA PIENA) ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29,90 €)")
    st.write("Il meglio per il tuo bimbo: 10 capi di grandi firme (Nike, Adidas, Ralph Lauren).")
    st.markdown("✨ **Qualità Oro:** Capi selezionati uno ad uno, sanificati a vapore.")
    if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg", caption="Esempio brand Premium")
    if st.button("ORDINA BOX PREMIUM"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
        st.balloons()

# --- 10. VETRINA (PUNTO 6 - ORA PIENA) ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Acquisto")
    st.markdown("""<div class="vision-card"><b>🛒 Prezzi Bomba:</b> I vestiti in vetrina li compri e sono tuoi per sempre. <b>Spedizione OMAGGIO sopra i 50€!</b></div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="vetrina-item">', unsafe_allow_html=True)
        if os.path.exists("scarpe.jpg"): st.image("scarpe.jpg")
        st.write("Scarpe Sportive<br><b>9,90 €</b>", unsafe_allow_html=True)
        st.button("Compra", key="v1")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="vetrina-item">', unsafe_allow_html=True)
        if os.path.exists("vestiti.jpg"): st.image("vestiti.jpg")
        st.write("Set Coordinato<br><b>14,50 €</b>", unsafe_allow_html=True)
        st.button("Compra", key="v2")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 11. ADMIN (PUNTO 7) ---
elif scelta == "🔐 Admin":
    st.title("Area Gestione 🔐")
    st.info("**Iscritti: 12** significa che 12 mamme si sono registrate all'app finora.")
    st.write(f"Posti occupati Promo Fondatrici: **{st.session_state.iscritti} / 50**")
    if st.session_state.user_data["cell"]:
        t = st.session_state.user_data["cell"]
        msg = urllib.parse.quote(f"Ciao {st.session_state.user_data['nome']}, sono di LoopBaby!")
        st.markdown(f'<a href="https://wa.me{t}?text={msg}"><button style="background:#25D366; color:white; border:none; padding:10px; border-radius:10px; width:100%;">📲 WHATSAPP</button></a>', unsafe_allow_html=True)
