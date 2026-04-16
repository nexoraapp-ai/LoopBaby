import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE & FIX ICONA ---
# Nota: page_icon usa il file locale, st.markdown forza il link per il cellulare
st.set_page_config(
    page_title="LoopBaby", 
    page_icon="favicon.ico", 
    layout="centered"
)

# Sostituisci 'NOME_REPO' con il nome reale del tuo repository su GitHub
URL_LOGO = "https://githubusercontent.com"

st.markdown(f"""
    <head>
        <link rel="icon" href="{URL_LOGO}" type="image/png">
        <link rel="apple-touch-icon" href="{URL_LOGO}">
    </head>
    <style>
    header {{ visibility: visible !important; }}
    footer {{ visibility: hidden; }}
    .stApp {{ background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }}
    
    /* Testi e Titoli */
    h1, h2, h3, p, span, label {{ color: #0d9488 !important; }}
    
    /* Pulsanti Custom */
    .stButton>button {{ 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }}
    
    /* Card Strutturate */
    .card {{ background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }}
    .promo-card {{ background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }}
    .price-tag {{ font-size: 1.2em; font-weight: bold; color: #e11d48 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE (GESTIONE DATI) ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "bimbo": "", "cellulare": "", "email": "",
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire"
    }

# --- 3. LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: 
                st.session_state.user_data["email"] = e
                st.session_state.autenticato = "utente"; st.rerun()
            
    with t2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Tuo Nome")
        c_m = st.text_input("N° Telefono")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 5.0)
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and c_m:
                tg = "0-1m" if p_b < 4.5 else "1-3m" if p_b < 5.5 else "3-6m" if p_b < 7.5 else "6-9m" if p_b < 9.0 else "12-24m"
                st.session_state.user_data.update({"nome": n_m, "bimbo": n_b, "cellulare": c_m, "taglia": tg})
                st.session_state.autenticato = "utente"
                st.session_state.iscritti += 1
                st.rerun()
    st.stop()

# --- 4. NAVIGAZIONE (SIDEBAR) ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    st.write(f"Ciao **{st.session_state.user_data['nome']}**! 🧸")
    scelta = st.radio("Menu:", ["🏠 Home", "📝 Profilo", "📦 Box Loop", "🛍️ Vetrina Shopping", "🔐 Area Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 5. HOME PAGE ---
if scelta == "🏠 Home":
    st.title("Benvenuta in LoopBaby! ✨")
    
    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <p><b>1ª BOX OMAGGIO E RITIRO GRATIS!</b><br>Riservato alle mamme che inviano 10+ capi.</p>
        <div style="font-size:1.5em; font-weight:800;">{st.session_state.iscritti} / 50 posti occupati</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h4>Come funziona? 🌿</h4>
        <p>1. Scegli una <b>Box</b> (Standard 19,90€ o Premium 29,90€).<br>
        2. Usala per 90 giorni.<br>
        3. Rendi tutto e ricevi la taglia successiva!</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. PROFILO (MODIFICABILE) ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_profilo"):
        u_nome = st.text_input("Nome Mamma", st.session_state.user_data["nome"])
        u_tel = st.text_input("Telefono", st.session_state.user_data["cellulare"])
        u_bimbo = st.text_input("Nome Bimbo/a", st.session_state.user_data["bimbo"])
        
        liste_t = ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"]
        default_t = liste_t.index(st.session_state.user_data["taglia"]) if st.session_state.user_data["taglia"] in liste_t else 0
        u_taglia = st.selectbox("Taglia Attuale", liste_t, index=default_t)
        
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": u_nome, "cellulare": u_tel, "bimbo": u_bimbo, "taglia": u_taglia})
            st.success("Dati aggiornati correttamente!")

# --- 7. BOX LOOP ---
elif scelta == "📦 Box Loop":
    st.title("Scegli il tuo Loop 📦")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card"><b>Box Standard</b><br><span class="price-tag">19,90€</span><br><small>10 capi stili misti</small></div>', unsafe_allow_html=True)
        if st.button("SCEGLI STANDARD"): st.toast("Box Standard selezionata!")
        
    with col2:
        st.markdown('<div class="card"><b>Box Premium</b><br><span class="price-tag">29,90€</span><br><small>10 capi Grandi Firme</small></div>', unsafe_allow_html=True)
        if st.button("SCEGLI PREMIUM"): st.toast("Box Premium selezionata!")

# --- 8. VETRINA SHOPPING ---
elif scelta == "🛍️ Vetrina Shopping":
    st.title("Vetrina LoopBaby 🛍️")
    st.warning("🚚 Spedizione GRATIS sopra i 50€!")
    
    prodotti = [
        {"n": "Set 3 Body Bio", "p": 18.00, "i": "🌱"},
        {"n": "Sacco Nanna 2.5 Tog", "p": 45.00, "i": "😴"},
        {"n": "Kit Accessori Pappa", "p": 22.00, "i": "🥣"}
    ]
    
    for item in prodotti:
        with st.container():
            c1, c2 = st.columns([2, 1])
            c1.markdown(f"**{item['i']} {item['n']}**")
            c1.markdown(f'<span class="price-tag">{item["p"]}0€</span>', unsafe_allow_html=True)
            if c2.button("Compra", key=item['n']):
                st.success(f"{item['n']} aggiunto al carrello!")

# --- 9. AREA ADMIN ---
elif scelta == "🔐 Area Admin":
    if st.session_state.autenticato != "admin":
        st.error("Accesso negato.")
    else:
        st.title("Pannello Gestione 🔐")
        st.write("Mamme iscritte al progetto:")
        
        # Simulazione Database
        data = [
            {"Mamma": "Chiara", "Tel": "3331234567", "Mail": "chiara@test.it", "Stato": "In Scadenza"},
            {"Mamma": "Federica", "Tel": "3409876543", "Mail": "fede@test.it", "Stato": "Attivo"}
        ]
        
        for m in data:
            with st.expander(f"👤 {m['Mamma']} - {m['Stato']}"):
                st.write(f"Telefono: {m['Tel']}")
                st.write(f"Email: {m['Mail']}")
                
                # WhatsApp Link
                wa_msg = urllib.parse.quote(f"Ciao {m['Mamma']}, qui LoopBaby! Il tuo box è quasi pronto per il cambio.")
                st.markdown(f"[💬 Contatta su WhatsApp](https://wa.me{m['Tel']}?text={wa_msg})")
                
                # Email Link
                mail_subj = urllib.parse.quote("Novità dal tuo LoopBaby")
                st.markdown(f"[✉️ Invia Email](mailto:{m['Mail']}?subject={mail_subj})")

