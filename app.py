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
    
    .vision-card, .card { background: white; padding: 20px; border-radius: 20px; border: 1px solid #0d9488; margin-bottom: 20px; }
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
if "carrello_vetrina" not in st.session_state: st.session_state.carrello_vetrina = []
if "user_data" not in st.session_state: 
    st.session_state.user_data = {
        "nome": "", "cognome": "", "bimbo": "", "nascita": datetime.now().date(), "cellulare": "", "peso": 4.0,
        "ha_ordinato": False, "data_ordine": None, "taglia": "da definire", "taglia_confermata": False
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
        st.write("### Diventa una Mamma Fondatrice")
        n_m = st.text_input("Nome")
        cg_m = st.text_input("Cognome")
        n_b = st.text_input("Nome del Bimbo/a")
        d_n = st.date_input("Data di Nascita", value=datetime.now().date())
        p_b = st.number_input("Peso attuale (kg)", 2.0, 20.0, 4.0)
        c_m = st.text_input("Cellulare")
        if st.button("REGISTRATI E BLOCCA PROMO"):
            if n_m and cg_m and c_m:
                st.session_state.user_data.update({
                    "nome": n_m, "cognome": cg_m, "bimbo": n_b, "nascita": d_n, 
                    "cellulare": c_m, "peso": p_b, "taglia": calcola_tg(p_b)
                })
                st.session_state.autenticato = "utente"
                st.session_state.primo_accesso = True
                st.rerun()
    st.stop()

# --- 5. CONFERMA/MODIFICA TAGLIA INIZIALE ---
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
    scelta = st.radio("Menu:", ["🏠 Home", "📝 Profilo", "📦 Box Standard", "💎 Box Premium", "🛍️ Vetrina", "🔐 Admin"])
    if st.button("Esci"): st.session_state.autenticato = False; st.rerun()

# --- 7. HOME PAGE (RIPRISTINATA) ---
if scelta == "🏠 Home":
    st.title(f"Benvenuta {st.session_state.user_data['nome']}! ✨")
    if st.session_state.user_data["ha_ordinato"]:
        giorni = (datetime.now() - st.session_state.user_data["data_ordine"]).days + 1
        st.markdown(f'<div class="tracker-box"><h4>🔄 Loop attivo</h4><h2>Giorno {giorni} di 90</h2></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="vision-card">
        <h4>Cos'è LoopBaby? 🌿</h4>
        <p>L'armadio circolare intelligente per il tuo bimbo <b>0-24 mesi</b>. <b>Risparmi, liberi spazio e rispetti il pianeta.</b></p>
        <hr>
        <p>📦 <b>Il Servizio:</b> Box da 19,90€ o 29,90€ compreso di trasporto. Invieremo 10 capi della taglia precisa al Locker più vicino a te.</p>
        <p>🔄 <b>Il Cambio:</b> Entro 90 giorni cambi taglia senza pagare il pacco di andata né quello di ritorno.</p>
        <p>🛑 <b>Reso Semplice:</b> Se decidi di non ordinare una nuova box, ritiriamo i vestiti al Locker con un ticket di soli 7,90€.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="promo-card">
        <h2>🚀 PROMO FONDATRICI</h2>
        <h3 style="color:#d97706 !important;">{st.session_state.iscritti} / 50 posti occupati</h3>
        <p>Inviaci 10 o più capi usati: <b>1ª Box Gratis</b> e <b>Ritiro OMAGGIO</b> pagato da noi!</p>
    </div>
    """, unsafe_allow_html=True)

# --- 8. PROFILO (FIXATO E MODIFICABILE) ---
elif scelta == "📝 Profilo":
    st.title("Il tuo Profilo 📝")
    with st.form("profilo_form"):
        u = st.session_state.user_data
        n = st.text_input("Nome", u["nome"])
        cg = st.text_input("Cognome", u["cognome"])
        b = st.text_input("Bimbo/a", u["bimbo"])
        dn = st.date_input("Data di Nascita", u["nascita"])
        tel = st.text_input("Telefono", u["cellulare"])
        tg_opzioni = ["0-1m", "1-3m", "3-6m", "6-9m", "12-24m"]
        tg_idx = tg_opzioni.index(u["taglia"]) if u["taglia"] in tg_opzioni else 0
        tg = st.selectbox("Taglia Attuale", tg_opzioni, index=tg_idx)
        
        if st.form_submit_button("SALVA MODIFICHE"):
            st.session_state.user_data.update({"nome": n, "cognome": cg, "bimbo": b, "nascita": dn, "cellulare": tel, "taglia": tg})
            st.success("Dati aggiornati!")

# --- 9. BOX STANDARD (RIPRISTINATA) ---
elif scelta == "📦 Box Standard":
    st.title("📦 Box Standard (19,90 €)")
    st.write("Scegli lo stile per i tuoi 10 capi:")
    for s, d in [("🌙 LUNA", "Colori neutri"), ("☀️ SOLE", "Colori vivaci"), ("☁️ NUVOLA", "Casual")]:
        with st.expander(s):
            st.write(d)
            st.write("(Caricheremo qui le 10 foto reali della box)")
            if st.button(f"Scegli {s}"):
                st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
                st.success(f"Box {s} ordinata!")

# --- 10. BOX PREMIUM ---
elif scelta == "💎 Box Premium":
    st.title("💎 Box Premium (29,90 €)")
    st.write("Box esclusiva con 10 vestiti di Grandi Firme. Caricheremo qui le 10 foto reali.")
    if st.button("ORDINA PREMIUM"):
        st.session_state.user_data.update({"ha_ordinato": True, "data_ordine": datetime.now()})
        st.success("Premium ordinata!")

# --- 11. VETRINA (OK) ---
elif scelta == "🛍️ Vetrina":
    st.title("🛍️ Vetrina Shopping")
    st.info("I capi rimangono a te! Gratis > 50€ o con una Box.")
    prezzi = [("Body Bio", 15.0), ("Tutina", 25.0)]
    for n, p in prezzi:
        st.write(f"**{n}** - {p}€")
        if st.button(f"Acquista {n}"): st.session_state.carrello_vetrina.append(p); st.toast("Aggiunto!")

# --- 12. ADMIN ---
elif scelta == "🔐 Admin":
    if st.session_state.autenticato == "admin":
        st.title("Area Admin 🔐")
        u = st.session_state.user_data
        if u["nome"]:
            g = (datetime.now() - u["data_ordine"]).days if u["ha_ordinato"] else 0
            st.write(f"Utente: {u['nome']} {u['cognome']} | Loop: Giorno {g}")
            if g >= 80:
                msg = urllib.parse.quote(f"Buongiorno {u['nome']}, mancano 10gg. Preparo nuova box?")
                st.markdown(f'<a href="https://wa.me{u["cellulare"]}?text={msg}" target="_blank"><button style="background:#25D366; color:white; border:none; padding:15px; border-radius:10px; width:100%;">📲 WHATSAPP</button></a>', unsafe_allow_html=True)
    else: st.error("Solo Admin")
