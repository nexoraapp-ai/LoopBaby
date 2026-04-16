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
    .price-tag { font-weight: bold; color: #e11d48; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSIONE ---
if "autenticato" not in st.session_state: st.session_state.autenticato = False
if "iscritti" not in st.session_state: st.session_state.iscritti = 12
if "primo_accesso" not in st.session_state: st.session_state.primo_accesso = False
if "carrello_vetrina" not in st.session_state: st.session_state.carrello_vetrina = []
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "cognome": "", "bimbo": "", "nascita": None, "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "tipo_box": "", "taglia": "da definire",
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
        n_m = st.text_input("Nome")
        cg_m = st.text_input("Cognome")
        n_b = st.text_input("Nome del Bimbo/a")
        d_n = st.date_input("Data di Nascita")
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0)
        c_m = st.text_input("Cellulare")
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and cg_m and c_m:
                st.session_state.user_data.update({"nome": n_m, "cognome": cg_m, "bimbo": n_b, "nascita": d_n, "cellulare": c_m, "peso": p_b, "taglia": calcola_tg(p_b)})
                st.session_state.autenticato = "utente"; st.session_state.primo_accesso = True; st.rerun()
    st.stop()

# --- 5. CONFERMA/MODIFICA TAGLIA INIZIALE ---
if st.session_state.primo_accesso and not st.session_state.user_data["taglia_confermata"]:
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    st.markdown(f'<div class="card" style="text-align: center;"><h4>Taglia suggerita per {st.session_state.user_data["bimbo"]}</h4><h2 style="color:#e11d48;">{st.session_state.user_data["taglia"]}</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("✅ CONFERMA"): st.session_state.user_data["taglia_confermata"] = True; st.session_state.primo_accesso = False; st.rerun()
    if c2.button("✏️ MODIFICA"):
        nuova = st.selectbox("Seleziona la taglia corretta:", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"])
        if st.button("SALVA TAGLIA"):
            st.session_state.user_data["taglia"] = nuova
            st.session_state.user_data["taglia_confermata"] = True
            st.session_state.primo_accesso = False; st.rerun()
    st.stop()

# --- 6. MENU ---
with st.sidebar:
    st.write(f"Ciao **{st.session_state.user_data['nome']}**!")
    scelta = st.radio("Naviga:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    if st.session_state.user_data["ha_ordinato"]:
        giorni = (datetime.now() - st.session_state.user_data["data_ordine"]).days + 1
        st.markdown(f'<div class="tracker-box"><h4>🔄 Loop attivo per {st.session_state.user_data["bimbo"]}</h4><h2>Giorno {giorni} di 90</h2></div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="card"><h4>LoopBaby: 0-24 Mesi 🌿</h4><p>Box da 19,90€ o 29,90€ con 10 capi. Cambio taglia gratis entro 90gg!</p></div>""", unsafe_allow_html=True)
    st.markdown(f'<div class="promo-card">🚀 <b>PROMO FONDATRICI:</b> {st.session_state.iscritti}/50 occupati</div>', unsafe_allow_html=True)

# --- 8. PROFILO (MODIFICABILE) ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("edit_profilo"):
        u = st.session_state.user_data
        n = st.text_input("Nome", u['nome'])
        cg = st.text_input("Cognome", u['cognome'])
        b = st.text_input("Bimbo/a", u['bimbo'])
        tel = st.text_input("Telefono", u['cellulare'])
        tg = st.selectbox("Taglia Attuale", ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"], index=["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"].index(u['taglia']))
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": n, "cognome": cg, "bimbo": b, "cellulare": tel, "taglia": tg})
            st.success("Profilo aggiornato!")

# --- 9. VETRINA ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Shopping")
    st.info("Capi che rimangono a te. Gratis > 50€ o con una Box!")
    capi = [("Body Bio", 15.0), ("Tutina", 25.0), ("Cappellino", 10.0)]
    for nome, prezzo in capi:
        with st.container():
            st.markdown(f"<div class='card'><b>{nome}</b> - <span class='price-tag'>{prezzo}€</span></div>", unsafe_allow_html=True)
            if st.button(f"Acquista {nome}"): 
                st.session_state.carrello_vetrina.append(prezzo)
                st.toast(f"{nome} aggiunto!")
    
    tot = sum(st.session_state.carrello_vetrina)
    sped = 0 if (tot >= 50 or st.session_state.user_data["ha_ordinato"]) else 7.90
    st.markdown(f"<div class='tracker-box'><b>Totale: {tot}€</b><br>Spedizione: {'GRATIS' if sped == 0 else str(sped)+'€'}</div>", unsafe_allow_html=True)

# --- 10. BOX ---
elif scelta in ["📦 Box Standard", "💎 Box Premium"]:
    prezzo = "19,90€" if "Standard" in scelta else "29,90€"
    st.title(f"{scelta} ({prezzo})")
    st.write("Caricheremo qui le 10 foto reali.")
    if st.button(f"ORDINA {scelta}"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now(), "tipo_box": scelta})
        st.success("Ordine effettuato!")

# --- 11. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Admin 🔐")
        u = st.session_state.user_data
        if u['nome']:
            giorni = (datetime.now() - u['data_ordine']).days if u['ha_ordinato'] else 0
            st.markdown(f"<div class='card'><b>{u['nome']} {u['cognome']}</b><br>Loop: Giorno {giorni} di 90</div>", unsafe_allow_html=True)
            if giorni >= 80:
                msg = urllib.parse.quote(f"Buongiorno {u['nome']}, mancano 10gg. Preparo una nuova box?")
                st.markdown(f'[![WhatsApp](https://shields.io)](https://wa.me{u["cellulare"]}?text={msg})', unsafe_allow_html=True)
    else: st.error("Solo Admin")
