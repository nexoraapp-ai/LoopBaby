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
    .tracker-box { background: #eef2ff; padding: 15px; border-radius: 20px; border: 2px solid #4338ca; margin-bottom: 20px; text-align: center; }
    .suggested-tag { font-size: 1.5em; font-weight: bold; color: #e11d48; background: #fff1f2; padding: 10px; border-radius: 10px; display: inline-block; margin: 10px 0; }
    .highlight { font-weight: bold; color: #0d9488; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "bimbo": "", "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire",
        "taglia_confermata": False
    }

def calcola_tg(peso):
    if peso < 4.5: return "0-1m"
    elif peso < 5.5: return "1-3m"
    elif peso < 7.5: return "3-6m"
    elif peso < 9.0: return "6-9m"
    else: return "12-24m"

# --- 4. ACCESSO E REGISTRAZIONE ---
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
        st.info("**Perché scegliere LoopBaby? 🌿**\n\n- 💰 **Risparmio:** Oltre 1.000€ l'anno in vestitini.\n- 📦 **Comodità:** Tutto tramite Locker vicino a casa tua.\n- 🌍 **Sostenibilità:** Basta sprechi tessili, entra nell'economia circolare.")
        n_m = st.text_input("Tuo Nome (Mamma)")
        c_m = st.text_input("Cellulare (per allert Locker)")
        n_b = st.text_input("Nome del Bimbo/a")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0)
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and c_m:
                st.session_state.user_data.update({"nome": n_m, "bimbo": n_b, "cellulare": c_m, "peso": p_b, "taglia": calcola_tg(p_b)})
                st.session_state.autenticato = "utente"
                st.session_state.primo_accesso = True
                st.session_state.iscritti += 1
                st.rerun()
    st.stop()

# --- 5. BENVENUTA (CONFERMA TAGLIA) ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <h4>Taglia suggerita per {st.session_state.user_data['bimbo']}</h4>
        <div class="suggested-tag">{st.session_state.user_data['taglia']}</div>
        <p>Calcolata sul peso di {st.session_state.user_data['peso']} kg</p>
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

# --- 6. SIDEBAR ---
with st.sidebar:
    st.write(f"Mamma: **{st.session_state.user_data['nome']}**")
    scelta = st.radio("Menu:", ["🏠 Home", "📝 Profilo", "📦 Box Loop", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")

    if st.session_state.user_data["ha_ordinato"]:
        inizio = st.session_state.user_data["data_ordine"]
        giorni = (datetime.now() - inizio).days + 1
        st.markdown(f'<div class="tracker-box"><h4>🔄 Loop attivo</h4><h2>Giorno {giorni} di 90</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4>Cos'è LoopBaby? 🌿</h4>
        <p>L'armadio circolare intelligente per il tuo bimbo. <b>Risparmi, liberi spazio e rispetti il pianeta.</b></p>
        <hr>
        <p>📦 <b>Come funziona:</b><br>
        Scegli la tua Box (Standard <span class="highlight">19,90€</span> o Premium <span class="highlight">29,90€</span>). 
        Il trasporto è <span class="highlight">sempre compreso</span>!</p>
        <p>👕 <b>Cosa ricevi:</b><br>
        Ti invieremo <b>10 capi</b> della taglia precisa di <b>{st.session_state.user_data['bimbo']}</b> al Locker più vicino a te.</p>
        <p>🔄 <b>Il Cambio Taglia:</b><br>
        Entro 90 giorni (o quando preferisci), ordina la taglia successiva. 
        <b>Non pagherai nulla</b>: né la spedizione della nuova box, né il reso della vecchia!</p>
        <p>🛑 <b>Se vuoi fermarti:</b><br>
        Se decidi di non ordinare una nuova box, pagherai solo un ticket di reso di <b>7,90€</b> e porterai i vestiti al Locker più comodo.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 posti occupati</h3>
        <p>Le prime 50 mamme che caricano il Loop con 10+ capi usati ricevono la 
        <b>1ª BOX GRATIS</b> e il <b>RITIRO A DOMICILIO OMAGGIO</b>. LoopBaby paga tutto!</p>
    </div>
    """, unsafe_allow_html=True)

# --- 8. PROFILO ---
elif scelta == "📝 Profilo":
    st.title("I tuoi dati 📝")
    st.write(f"Mamma: **{st.session_state.user_data['nome']}**")
    st.write(f"Bimbo: **{st.session_state.user_data['bimbo']}**")
    st.write(f"Taglia attuale: **{st.session_state.user_data['taglia']}**")

# --- 9. BOX LOOP ---
elif scelta == "📦 Box Loop":
    st.title("Scegli il tuo Box 📦")
    st.markdown('<div class="card"><b>Standard Loop</b> (19,90€)<br>10 capi stili misti igienizzati.</div>', unsafe_allow_html=True)
    if st.button("ORDINA STANDARD"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
        st.success("Ordine confermato! Corri in Home a vedere il tuo Loop.")

# --- 10. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        cel = st.session_state.user_data["cellulare"]
        if cel:
            wa_text = urllib.parse.quote(f"Ciao {st.session_state.user_data['nome']}! Qui LoopBaby, come va il Loop di {st.session_state.user_data['bimbo']}?")
            st.markdown(f'<a href="https://wa.me{cel}?text={wa_text}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%; cursor:pointer;">📲 CONTATTA SU WHATSAPP</button></a>', unsafe_allow_html=True)
