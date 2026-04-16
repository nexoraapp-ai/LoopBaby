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
    .price-tag { font-weight: bold; color: #e11d48; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "carrello_vetrina" not in st.session_state: st.session_state.carrello_vetrina = 0
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

# --- 4. ACCESSO E REGISTRAZIONE ---
if not st.session_state.autenticato:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)
    t1, t2 = st.tabs(["Accedi", "Registrati"])
    
    with t2:
        st.info("**Perché scegliere LoopBaby? 🌿**\nRisparmio, spazio e sostenibilità per bimbi 0-24 mesi.")
        n_m = st.text_input("Tuo Nome (Mamma)")
        n_b = st.text_input("Nome del Bimbo/a")
        d_n = st.date_input("Data di Nascita", min_value=datetime(2022, 1, 1))
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0)
        c_m = st.text_input("Cellulare")
        if st.button("REGISTRATI"):
            if n_m and n_b:
                st.session_state.user_data.update({
                    "nome": n_m, "bimbo": n_b, "nascita": d_n, "cellulare": c_m, 
                    "peso": p_b, "taglia": calcola_tg(p_b)
                })
                st.session_state.autenticato = "utente"; st.session_state.primo_accesso = True; st.session_state.iscritti += 1; st.rerun()
    st.stop()

# --- 5. CONFERMA TAGLIA ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Taglia suggerita per {st.session_state.user_data["bimbo"]}</h4><h2 style="color:#e11d48;">{st.session_state.user_data["taglia"]}</h2><p>Basata su {st.session_state.user_data["peso"]}kg</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("✅ CONFERMA"): st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    if c2.button("✏️ MODIFICA"):
        nuova = st.selectbox("Scegli taglia", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.button("SALVA"): st.session_state.user_data["taglia"] = nuova; st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU ---
with st.sidebar:
    st.write(f"Mamma: **{st.session_state.user_data['nome']}**")
    st.write(f"Bimbo: **{st.session_state.user_data['bimbo']}**")
    scelta = st.radio("Menu:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    if st.session_state.user_data["ha_ordinato"]:
        giorni = (datetime.now() - st.session_state.user_data["data_ordine"]).days + 1
        st.markdown(f'<div class="tracker-box"><h4>🔄 Loop attivo per {st.session_state.user_data["bimbo"]}</h4><h2>Giorno {giorni} di 90</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4>LoopBaby: Vestiti Circolari 0-24 Mesi 🌿</h4>
        <p>Scegli una Box (19,90€ o 29,90€) con <b>10 capi</b> scelti per te e inviati al <b>Locker</b> più vicino.</p>
        <p>🔄 <b>Reso Gratis</b> se rinnovi la taglia. Se vuoi fermarti, rendi tutto al Locker con un ticket di soli <b>7,90€</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="promo-card"><h2>🚀 PROMO FONDATRICI</h2><h3>{st.session_state.iscritti} / 50 mamme</h3><p>Inviaci 10 capi usati: 1ª Box Gratis e ritiro a casa pagato da noi!</p></div>', unsafe_allow_html=True)

# --- 8. BOX STANDARD (3 STILI) ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19,90 €)")
    st.write("Scegli lo stile per i 10 capi di questa taglia:")
    stili = [("🌙 LUNA", "Colori neutri e delicati"), ("☀️ SOLE", "Colori vivaci e allegri"), ("☁️ NUVOLA", "Vestiti casual e pratici")]
    for nome, desc in stili:
        with st.expander(nome):
            st.write(desc)
            st.write("(Qui caricheremo le 10 foto reali)")
            if st.button(f"Scegli Box {nome}"):
                st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
                st.success(f"Hai scelto lo stile {nome}! Preparazione in corso.")

# --- 9. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29,90 €)")
    st.write("Un'unica box esclusiva con 10 vestiti di **Alta Gamma** (Grandi Firme).")
    if st.button("ORDINA PREMIUM"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
        st.balloons()

# --- 10. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Shopping")
    st.info("I vestiti in vetrina sono tuoi per sempre! Spedizione GRATIS sopra i 50€ o se acquistati con una Box.")
    
    prezzo_capo = 15.0 # Esempio
    st.write(f"Capo Esempio: **Giacchino Bio** - <span class='price-tag'>{prezzo_capo}€</span>", unsafe_allow_html=True)
    if st.button("Aggiungi al carrello"):
        st.session_state.carrello_vetrina += prezzo_capo
        st.toast("Aggiunto!")

    st.divider()
    tot = st.session_state.carrello_vetrina
    sped = 0 if (tot >= 50 or st.session_state.user_data["ha_ordinato"]) else 7.90
    st.write(f"Totale Prodotti: {tot}€")
    st.write(f"Spedizione: {'GRATIS' if sped == 0 else str(sped) + '€'}")
    if st.button("PROCEDI ALL'ACQUISTO"): st.success("Ordine Vetrina ricevuto!")

# --- 11. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        cel = st.session_state.user_data["cellulare"]
        if cel:
            wa = urllib.parse.quote(f"Ciao {st.session_state.user_data['nome']}! Novità per il Loop di {st.session_state.user_data['bimbo']}.")
            st.markdown(f'<a href="https://wa.me{cel}?text={wa}"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%;">📲 WHATSAPP</button></a>', unsafe_allow_html=True)
