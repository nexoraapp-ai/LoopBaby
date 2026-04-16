import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="LoopBaby", page_icon="logo.png", layout="centered")

# --- 2. STILE GRAFICO ---
st.markdown("""
    <style>
    header { visibility: visible !important; }
    footer { visibility: hidden; }
    .stApp { background-color: #f0fdfa !important; max-width: 500px; margin: 0 auto; }
    h1, h2, h3, h4, p, span, label, div { color: #0d9488 !important; }
    
    .stButton>button { 
        border-radius: 30px !important; height: 3.5em !important; font-weight: 800 !important; 
        background: linear-gradient(135deg, #7fa082 0%, #0d9488 100%) !important; 
        color: white !important; border: none !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(13,148,136,0.3) !important;
    }
    
    .card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
    .promo-card { background: #fef3c7; padding: 20px; border-radius: 20px; border: 2px solid #d97706; text-align: center; margin-bottom: 20px; }
    .tracker-box { background: white; padding: 15px; border-radius: 20px; border: 2px solid #0d9488; margin-bottom: 20px; text-align: center; }
    .price-tag { font-weight: bold; color: #e11d48; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "bimbo": "", "nascita": None, "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire",
        "taglia_confermata": False
    }

def calcola_tg(peso):
    if peso < 4.5: return "0-1m"
    elif peso < 5.5: return "1-3m"
    elif peso < 7.5: return "3-6m"
    elif peso < 9.0: return "6-9m"
    else: return "12-24m"

# --- 4. LOGIN / REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("ENTRA"):
            if e == "admin" and p == "baby2024": st.session_state.autenticato = "admin"; st.rerun()
            elif e: st.session_state.autenticato = "utente"; st.rerun()
            
    with t2:
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Tuo Nome (Mamma)")
        n_b = st.text_input("Nome del Bimbo/a")
        d_n = st.date_input("Data di Nascita", min_value=datetime(2022, 1, 1))
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0)
        c_m = st.text_input("Cellulare (per allert Locker)")
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and c_m:
                st.session_state.user_data.update({
                    "nome": n_m, "bimbo": n_b, "nascita": d_n, "cellulare": c_m, 
                    "peso": p_b, "taglia": calcola_tg(p_b)
                })
                st.session_state.autenticato = "utente"; st.session_state.primo_accesso = True; st.rerun()
    st.stop()

# --- 5. CONFERMA TAGLIA DOPO LOGIN ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h4>Taglia suggerita per {st.session_state.user_data['bimbo']}</h4>
        <div class="suggested-tag" style="font-size:2em; color:#e11d48; font-weight:bold;">{st.session_state.user_data['taglia']}</div>
        <p>In base al peso di {st.session_state.user_data['peso']} kg</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("✅ CONFERMA"):
        st.session_state.user_data["taglia_confermata"] = True
        st.session_state.primo_accesso = False; st.rerun()
    if c2.button("✏️ MODIFICA"):
        nuova = st.selectbox("Scegli taglia", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.button("SALVA"):
            st.session_state.user_data["taglia"] = nuova
            st.session_state.user_data["taglia_confermata"] = True
            st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=120)
    st.write(f"Mamma: **{st.session_state.user_data['nome']}**")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")

    if st.session_state.user_data["ha_ordinato"]:
        giorni = (datetime.now() - st.session_state.user_data["data_ordine"]).days + 1
        st.markdown(f'<div class="tracker-box"><h4>🔄 Loop attivo per {st.session_state.user_data["bimbo"]}</h4><h2>Giorno {giorni} di 90</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4>Cos'è LoopBaby? 🌿</h4>
        <p>L'armadio circolare intelligente <b>0-24 mesi</b>. Risparmi, liberi spazio e rispetti il pianeta.</p>
        <hr>
        <p>📦 <b>Il Servizio:</b> Box da 19,90€ o 29,90€ compreso di trasporto. Invieremo 10 capi della taglia precisa al Locker più vicino a te.</p>
        <p>🔄 <b>Il Cambio:</b> Entro 90 giorni cambi taglia senza pagare il pacco di andata né quello di ritorno.</p>
        <p>🛑 <b>Reso Semplice:</b> Se non vuoi rinnovare, ritiriamo i vestiti al Locker per soli 7,90€.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 mamme</h3>
        <p>Inviaci 10 o più capi usati: <b>1ª Box Gratis</b> e <b>Ritiro a casa OMAGGIO</b> pagato da noi!</p>
    </div>
    """, unsafe_allow_html=True)

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.container():
        st.markdown(f"""
        <div class="card">
            <p><b>Mamma:</b> {st.session_state.user_data['nome']}</p>
            <p><b>Bimbo/a:</b> {st.session_state.user_data['bimbo']}</p>
            <p><b>Data di Nascita:</b> {st.session_state.user_data['nascita']}</p>
            <p><b>Telefono:</b> {st.session_state.user_data['cellulare']}</p>
            <p><b>Taglia Attuale:</b> {st.session_state.user_data['taglia']}</p>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Modifica Dati"):
        st.info("In questa sezione potrai presto modificare i tuoi dati direttamente.")

# --- 9. BOX STANDARD ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19,90 €)")
    st.write("Scegli lo stile per i tuoi 10 capi:")
    for stile, desc in [("🌙 LUNA", "Colori neutri"), ("☀️ SOLE", "Colori vivaci"), ("☁️ NUVOLA", "Casual")]:
        with st.expander(stile):
            st.write(desc)
            st.write("(Qui caricheremo le 10 foto reali della box)")
            if st.button(f"Scegli {stile}"):
                st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
                st.success(f"Box {stile} ordinata!")

# --- 10. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29,90 €)")
    st.markdown("""
    <div class="card">
        <p>Un'unica box esclusiva con <b>10 vestiti di Alta Gamma (Grandi Firme)</b>.</p>
        <p><i>Caricheremo qui le 10 foto reali dei capi inclusi.</i></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("ORDINA PREMIUM"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
        st.balloons()
        st.success("Box Premium ordinata! Preparati allo stile.")

# --- 11. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Shopping")
    st.info("I capi in vetrina rimangono a te! Spedizione GRATIS sopra i 50€.")
    st.write("Qui caricheremo le foto e i prezzi di ogni singolo capo.")

# --- 12. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Area Admin 🔐")
        st.write(f"Mamme iscritte: **{st.session_state.iscritti}**")
        
        # Tabella rapida
        df_utenti = pd.DataFrame([{
            "Mamma": st.session_state.user_data['nome'],
            "Bimbo": st.session_state.user_data['bimbo'],
            "Taglia": st.session_state.user_data['taglia'],
            "Tel": st.session_state.user_data['cellulare']
        }])
        st.table(df_utenti)
        
        cel = st.session_state.user_data["cellulare"]
        if cel:
            wa_text = urllib.parse.quote(f"Ciao {st.session_state.user_data['nome']}! Qui LoopBaby...")
            st.markdown(f'<a href="https://wa.me{cel}?text={wa_text}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%; cursor:pointer;">📲 CONTATTA SU WHATSAPP</button></a>', unsafe_allow_html=True)
    else:
        st.error("Accesso riservato all'amministratore.")
